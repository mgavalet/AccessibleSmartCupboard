# Learning imports 
import numpy as np
import cv2
import os
from tensorflow import keras
import tensorflow as tf
from collections import Counter
import shutil
import requests
import time 
from termcolor import colored

path_of_classfication_model = '/home/marios/Downloads/afterDemo_12products.h5'
path_localizer = '/home/marios/Downloads/object_detection_mobile_object_localizer_v1_1_default_1.tflite'
class_names = ['Beans', 'Coffee', 'Corn', 'Mayo', 'Merenda',
                   'Mushroom', 'Mustard', 'Rice', 'Salt', 'Sugar', 'Tomato', 'Vinegar']

img_height = 500 # constant 
img_width = 300 # constant                    
IMG_HEIGHT_LOCALIZER = 192  # constant
IMG_WIDTH_LOCALIZER = 192  # constant
OFFSET = 25  # global and constant
LOCALIZER_THRESHOLD = 0.3 # constant from 0.4 to 0.3
X1 = 300  # constant --> x that start filling white the left edge of the image
STEP = 5 # 5 mm steps for the camera

def initializeVar(shelf):
    
    global counter_run
    global num_distinct_items
    global flag_left_side_now
    global flag_left_side_before
    global lazer_fails_counter
    global x_canditate
    global temp_list
    global xCoordinates

    
    counter_run = 0  # initialize
    num_distinct_items = 0  # initialize
    flag_left_side_now = False  # initialize
    flag_left_side_before = True # initialize ---> lie just to get the first lazer detection
    lazer_fails_counter = 0  # initialize
    x_canditate = 0  # initialize --> just a lie
    temp_list = []  # initialize
    
    if shelf == "down":
        xCoordinates = []  # initialize

def getNumPixels(currentX): # how many pixels to cut after x = 300 
    alpha = 1.3125
    beta = -343.75
    numPixels = (alpha*currentX)+beta  # y=a*x+b
    return numPixels

def Scanning(main_path,cupboardIP):
    global counter_run
    global num_distinct_items
    global flag_left_side_now
    global flag_left_side_before
    global lazer_fails_counter
    global x_canditate
    global temp_list
    global xCoordinates
    
    for numMoves in range(0,77): # 76 moves = 380/5
    
        if numMoves % 7 == 0 : # every 7 camera moves and numMoves != 0  
            requests.post('http://' + cupboardIP+ '/lights/lightOneMoreLed')
            print("one more led is on ...")

        currentX = STEP * numMoves
        
        res = requests.post('http://' + cupboardIP+ '/camera/horizontallyBy', json={"x" : STEP})

        counter_run += 1  # for naming different images while saving

        capture_response_req = requests.post('http://' + cupboardIP+ '/camera/capture')
        time.sleep(0.5) # debug
        
        image_bytes = capture_response_req.content  
        nparr = np.frombuffer(image_bytes, np.uint8) #Use frombuffer instead of fromstring
        
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rotated_img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # rotate clockwise

        original_height = rotated_img.shape[0]
        original_width = rotated_img.shape[1]
        x_lazer = int(original_width/2)

        input_image = rotated_img
        if currentX >= X1:  # apply cutting
            cuttingPixels = getNumPixels(currentX)

            cv2.rectangle(input_image, (0, 0), (int(
                cuttingPixels), original_height), (255, 255, 255), -1)  # fill rectangle with white

        input_image_copy = input_image.copy()
        cv2.line(input_image_copy, (x_lazer + OFFSET, 0),
                    (x_lazer + OFFSET, original_height), 2)  # draw line

        # Load localizer
        interpreter = tf.lite.Interpreter(model_path=path_localizer)

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.allocate_tensors()

        img_localizer = cv2.resize(
            input_image, (IMG_WIDTH_LOCALIZER, IMG_HEIGHT_LOCALIZER))  # input image

        interpreter.set_tensor(input_details[0]['index'], [img_localizer])

        interpreter.invoke()  # Run localizer

        detection_boxes = interpreter.get_tensor(output_details[0]["index"])
        detection_scores = interpreter.get_tensor(output_details[2]["index"])


        my_boxes = np.empty((0, 4))
        for index, score in enumerate(detection_scores[0]):
            if score > LOCALIZER_THRESHOLD :
                # reshape (4,) to (1,4)
                rectangular = np.reshape(detection_boxes[0][index], (1, 4))
                
                # Get the x,y coordinates
                y_min = int(max(1, (rectangular[0][0] * original_height)))
                x_min = int(max(1, (rectangular[0][1] * original_width)))
                y_max = int(min(original_height, (rectangular[0][2] * original_height)))
                x_max = int(min(original_width, (rectangular[0][3] * original_width)))    


                checkWidth = x_max - x_min
                checkHeight = y_max - y_min
                
                if checkHeight > 230 or checkWidth > 160: # maybe "or" here 
                    # print(colored("Too big RECTANGLE ... SKIP" , "red")) # debug 
                    continue # go to the next object

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

            if (x_min < x_lazer + OFFSET) and (x_lazer + OFFSET < x_max):
                lazer_rect = np.reshape(my_boxes[box][:], (1, 4))
                lazer_boxes = np.append(lazer_boxes, lazer_rect, axis=0)
                x_differences.append(abs(x_lazer - x_max))
                num_lazer_items += 1
        
        print('Lazer has detected : ', num_lazer_items)
        print()

        # SHOW IMAGE
        cv2.imshow('image window', input_image_copy) # debug
        cv2.waitKey(0) # debug
        cv2.destroyAllWindows() # debug

        if num_lazer_items != 0:
            maxIdx = np.argmax(x_differences)

            y_min = int(max(1, (lazer_boxes[maxIdx][0] * original_height)))
            x_min = int(max(1, (lazer_boxes[maxIdx][1] * original_width)))
            y_max = int(
                min(original_height, (lazer_boxes[maxIdx][2] * original_height)))
            x_max = int(
                min(original_width, (lazer_boxes[maxIdx][3] * original_width)))
            crop_image = input_image[y_min:y_max, x_min:x_max]

            capturedImage_height = crop_image.shape[0]             
            capturedImage_width = crop_image.shape[1]

            if capturedImage_height > 230 or capturedImage_width > 160: 
                print("Too big foto ... continueee") # debug 
                continue # go to the next capture 

            dx = x_max - x_min
            if x_lazer < (x_min + (dx/3)):
                flag_left_side_now = True
            else:
                flag_left_side_now = False

            if (flag_left_side_before is True) and (flag_left_side_now is False):
                
                num_distinct_items += 1
                # debug
                print(colored('New different item has been detected !', 'green'))
                print('New item starts at :', colored('%s' % currentX, 'blue'))
                print('\n')

                if len(temp_list) == 0:
                    temp_list.append(currentX)  # vale start
                    if x_canditate != 0:
                        temp_list.append(x_canditate)  # vale kai to finish
                        temp_list = []  # reset

                elif len(temp_list) == 1:
                    temp_list.append(x_canditate)  # vale to finish
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


def Prediction(main_path,cupboardIP):
    # Load classficaton model
    model = keras.models.load_model(path_of_classfication_model)
    result_list = [] # initialize 
    print()
    print()
    print()
    print()
    
    counter_items_found = 0 

    for folderShelf in sorted(os.listdir(main_path)): # gia kathe rafi 
        
        print()
        print("shelf folder : " ,folderShelf)


        for count , folder in enumerate(sorted(os.listdir(os.path.join(main_path,folderShelf)))): # gia kathe antikeimeno 
            counter_items_found += 1  
            results = {} # initialize
            
            # Initialize an array
            classification_results = []
            for foto in sorted(os.listdir(os.path.join(main_path,folderShelf,folder))):

                img = keras.preprocessing.image.load_img(os.path.join(
                    main_path,folderShelf,folder, foto), target_size=(img_height, img_width))
                img_array = keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)  # Create a batch

                predictions_score = model(img_array)  # Predict

                predictions_prob = tf.nn.softmax(predictions_score[0]).numpy()
                predicted_label = np.argmax(predictions_prob)
                predicted_class = class_names[predicted_label]

                classification_results.append(predicted_class)

            items_frequncies = Counter(classification_results)
            most_frequent_item = items_frequncies.most_common(1)[0][0]


            print('Position :', count+1, 'Item detected : ', most_frequent_item)

            if xCoordinates[counter_items_found - 1][0] >= 20 and xCoordinates[counter_items_found - 1][1] <= 110 :
                results['Quantity'] = requests.post('http://' + cupboardIP + '/weight/calculateWeight').content
            else:
                results['Label'] = most_frequent_item
                results['Cupboard'] = 1 
                results['Shelf'] = folderShelf 
                results['x_start'] = xCoordinates[counter_items_found - 1][0] 
                results['x_end'] = xCoordinates[counter_items_found - 1][1]
                results['Quantity'] = "unknown" 

            result_list.append(results.copy())

    return result_list



main_path = '/home/marios/Desktop/learningCupboard/lazer_detect'
cupboardControllerServer_IP = '139.91.96.156'

initializeVar("down")
Scanning(main_path,cupboardControllerServer_IP)
