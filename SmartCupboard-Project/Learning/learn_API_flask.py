from flask import Flask, jsonify
import cv2
import os
import numpy as np
from numpy.core.numeric import _frombuffer
import requests
import tensorflow as tf
import time
import keras
from collections import Counter
from termcolor import colored

def getNumPixels(currentX):
    alpha = 1.3125
    beta = -343.75
    numPixels = (alpha*currentX)+beta  # y=a*x+b
    return numPixels


POST_dataToSend = {} # initialize dictionary / json

cupboardControllerServer_IP = '139.91.96.156'

app = Flask(__name__)


@app.route('/learn/' , methods = ['GET'])
def learn_func():

    print("Camera homing ...") 
    requests.post('http://' + cupboardControllerServer_IP+ '/camera/dohoming')
    print(colored("Done ..." , 'green')) 
    
    print("Door homing ...") 
    requests.post('http://' + cupboardControllerServer_IP+ '/door/homing')
    print(colored("Done ..." , 'green')) 
    
    print("Door is light up yellow ...") 
    requests.post('http://' + cupboardControllerServer_IP+ '/lights/ConstantDoor', json={"color" : "yellow"})
    print(colored("Done ..." , 'green')) 
    
    
    # # Path to save the captured picture
    main_path = '/home/marios/Desktop/learningCupboard/lazer_detect'
    path_of_classfication_model = '/home/marios/Downloads/afterDemo_12products.h5'
    path_localizer = '/home/marios/Downloads/object_detection_mobile_object_localizer_v1_1_default_1.tflite'

    img_height_localizer = 192  # constant
    img_width_localizer = 192  # constant

    counter_run = 0  # initialize
    num_distinct_items = 0  # initialize
    flag_left_side_now = False  # initialize
    # initialize ---> lie just to get the first lazer detection
    flag_left_side_before = True
    
    POST_dataToSend['framesize'] = 6

    print("Set framesize of camera to 6 ...") 
    res = requests.post('http://' + cupboardControllerServer_IP+ '/camera/setFramesize', json=POST_dataToSend)    
    time.sleep(2)  # Wait some seconds SO not to get a dark image
    print(colored("Done ..." , 'green')) 
        
    starting_x = 0
    starting_y = 30
    POST_dataToSend['x'] = starting_x
    POST_dataToSend['y'] = starting_y
    
    print("Move camera to (0,30) position ...") 
    res = requests.post('http://' + cupboardControllerServer_IP+ '/camera/ToPosition', json=POST_dataToSend)
    print(colored("Done ..." , 'green')) 
    
    localizer_threshold = 0.4
    x1 = 300  # constant --> x that start filling white the left edge of the image
    lazer_fails_counter = 0  # initialize
    offset = 25  # global and constant

    start_time = time.time()  # starting time for scanning

    x_canditate = 0  # initialize --> just a lie
    xCoordinates = []  # initialize
    temp_list = []  # initialize
    
    step = 5 # 5 mm steps for the camera

    # for currentX in range(num_x_init, 380, 5):
    for numMoves in range(0,76): # 76 moves = 380/5
        
        currentX = step * numMoves
        print("currentX is : " , currentX) 
        POST_dataToSend['x'] = step
        
        res = requests.post('http://' + cupboardControllerServer_IP+ '/camera/horizontallyBy', json=POST_dataToSend)

        counter_run += 1  # for naming different images while saving

        capture_response_req = requests.post('http://' + cupboardControllerServer_IP+ '/camera/capture', json=POST_dataToSend)
        time.sleep(0.5) # debug
        
        image_bytes = capture_response_req.content  
        nparr = np.frombuffer(image_bytes, np.uint8) #Use frombuffer instead
        
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rotated_img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # clockwise

        original_height = rotated_img.shape[0]
        original_width = rotated_img.shape[1]
        x_lazer = int(original_width/2)

        input_image = rotated_img
        if currentX >= x1:  # apply cutting
            cuttingPixels = getNumPixels(currentX)

            cv2.rectangle(input_image, (0, 0), (int(
                cuttingPixels), original_height), (255, 255, 255), -1)  # fill rectangle with white

        input_image_copy = input_image.copy()
        cv2.line(input_image_copy, (x_lazer + offset, 0),
                 (x_lazer + offset, original_height), 2)  # draw line

        # Load localizer
        interpreter = tf.lite.Interpreter(model_path=path_localizer)

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.allocate_tensors()

        img_localizer = cv2.resize(
            input_image, (img_width_localizer, img_height_localizer))  # input image

        interpreter.set_tensor(input_details[0]['index'], [img_localizer])

        interpreter.invoke()  # Run localizer

        detection_boxes = interpreter.get_tensor(output_details[0]["index"])
        detection_scores = interpreter.get_tensor(output_details[2]["index"])

        my_boxes = np.empty((0, 4))
        for index, score in enumerate(detection_scores[0]):
            if score > localizer_threshold:
                # reshape (4,) to (1,4)
                rectangular = np.reshape(detection_boxes[0][index], (1, 4))
                my_boxes = np.append(my_boxes, rectangular, axis=0)

        num_boxes = my_boxes.shape[0]

        num_lazer_items = 0  # initialize
        x_differences = []  # initialize ---> to get only the most right lazer foto

        lazer_boxes = np.empty((0, 4))  # initialize

        for box in range(0, num_boxes):
            # Get the x,y coordinates
            y_min = int(max(1, (my_boxes[box][0] * original_height)))
            x_min = int(max(1, (my_boxes[box][1] * original_width)))
            y_max = int(
                min(original_height, (my_boxes[box][2] * original_height)))
            x_max = int(
                min(original_width, (my_boxes[box][3] * original_width)))

            cv2.rectangle(input_image_copy, (x_min, y_min),
                          (x_max, y_max), (255, 255, 255), 1)  # draw rectangle

            if (x_min < x_lazer + offset) and (x_lazer + offset < x_max):
                lazer_rect = np.reshape(my_boxes[box][:], (1, 4))
                lazer_boxes = np.append(lazer_boxes, lazer_rect, axis=0)
                x_differences.append(abs(x_lazer - x_max))
                num_lazer_items += 1

        # SHOW IMAGE
        cv2.imshow('image window', input_image_copy) 
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        
        if num_lazer_items != 0:
            maxIdx = np.argmax(x_differences)

            y_min = int(max(1, (lazer_boxes[maxIdx][0] * original_height)))
            x_min = int(max(1, (lazer_boxes[maxIdx][1] * original_width)))
            y_max = int(
                min(original_height, (lazer_boxes[maxIdx][2] * original_height)))
            x_max = int(
                min(original_width, (lazer_boxes[maxIdx][3] * original_width)))
            crop_image = input_image[y_min:y_max, x_min:x_max]

            dx = x_max - x_min
            if x_lazer < (x_min + (dx/3)):
                flag_left_side_now = True
            else:
                flag_left_side_now = False

            if (flag_left_side_before is True) and (flag_left_side_now is False):
                num_distinct_items += 1

                print(colored('New different item has been detected !', 'green'))
                print('New item starts at :', colored('%s' % currentX, 'blue'))
                print('\n')

                if len(temp_list) == 0:
                    temp_list.append(currentX)  # insert start
                    if x_canditate != 0:
                        temp_list.append(x_canditate)  # insert finish
                        temp_list = []  # reset

                elif len(temp_list) == 1:
                    temp_list.append(x_canditate)  # insert finish
                    xCoordinates.append(temp_list)  # push to main list
                    temp_list = []  # reset
                    temp_list.append(currentX)

                if not os.path.exists(os.path.join(main_path, 'item'+str(num_distinct_items))):
                    os.makedirs(os.path.join(
                        main_path, 'item'+str(num_distinct_items)))
                cv2.imwrite(os.path.join(main_path, 'item'+str(num_distinct_items),
                            'foto' + str(counter_run) + '.jpg'), crop_image)
            else:
                cv2.imwrite(os.path.join(main_path, 'item'+str(num_distinct_items),
                            'foto' + str(counter_run) + '.jpg'), crop_image)

            if lazer_fails_counter >= 1:
                if flag_left_side_before == flag_left_side_now:  # then it is a false alarm
                    print('Localizer failed')
                else:  # then it found empty space
                    print('It was empty space \n')
                    print(colored('Previous item was finished at : %s' %
                          x_canditate, 'yellow'))

                lazer_fails_counter = 0  # re-reset the counter to zero

            flag_left_side_before = flag_left_side_now

        else:
            lazer_fails_counter += 1  # increase counter

            if lazer_fails_counter == 1:
                x_canditate = currentX  # canditate for ending point of an item

    # for the last item
    if len(temp_list) != 2:
        temp_list.append(x_canditate)  # add last x_finsh to temp list
        xCoordinates.append(temp_list)  # push

    print('xCoordinates :', xCoordinates)  # debug

    finish_time = time.time()  # starting time for prediction  & finish of scanning
    print('\n')

    print(
        "Scanning duration ---> {:.2f} seconds " .format(finish_time - start_time))
    
    print(colored('Scanning is over ...' , 'green'))
    print(colored('Prediction time ...' , 'green'))
    print()

    time.sleep(2)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    img_height = 500
    img_width = 300
    class_names = ['Beans', 'Coffee', 'Corn', 'Mayo', 'Merenda',
                   'Mushroom', 'Mustard', 'Rice', 'Salt', 'Sugar', 'Tomato', 'Vinegar']

    # Load classficaton model
    model = keras.models.load_model(path_of_classfication_model)
    items_found_list = []  # initialize , new line here
    for count, folder in enumerate(sorted(os.listdir(main_path))):
        # Initialize an array
        classification_results = []
        for foto in sorted(os.listdir(os.path.join(main_path, folder))):
            img = keras.preprocessing.image.load_img(os.path.join(
                main_path, folder, foto), target_size=(img_height, img_width))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch

            predictions_score = model(img_array)  # Predict

            predictions_prob = tf.nn.softmax(predictions_score[0]).numpy()
            predicted_label = np.argmax(predictions_prob)
            predicted_max_propability = np.amax(predictions_prob) # unused
            predicted_class = class_names[predicted_label]

            classification_results.append(predicted_class)

        items_frequncies = Counter(classification_results)
        most_frequent_item = items_frequncies.most_common(1)[0][0]

        print('Position :', count+1, 'Item detected : ', most_frequent_item)

        items_found_list.append(most_frequent_item)  # add to list

    # Create a json - dictionary object to return
    result_list = [] # initialize 
    results = {} # initialize

    print(items_found_list) # debug

    print("length of items_found_list is :" , len(items_found_list)) # debug
    print("length of xCoordinates is :" , len(xCoordinates)) # debug

    for idx, product in enumerate(items_found_list):
        results['object'] = product
        results['position'] = {} # initialize 

        results['position']['Cupboard'] = 1 # change in future
        results['position']['Shelf'] = 1 # change in future --- 1 = down and 0 = up shelf
        results['position']['x_start'] = xCoordinates[idx][0]
        results['position']['x_end'] = xCoordinates[idx][1]

        result_list.append(results.copy())
    

    result_list = jsonify(result_list) # make the list a Response.instance type
    
    requests.post('http://' + cupboardControllerServer_IP + '/lights/switchoff' ,json={"ledstripeId" : 0}) #then and switch off door lights !!! 

    
    
    return result_list # type ---> <class 'flask.wrappers.Response'>
    
    
if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable tf/keras warnings -- not working

    # parameters of run() : host .port, options
    app.run(debug=True,host='0.0.0.0',port=5004)  # Run server from anywhere -- MariosPC -- ifconfig that 