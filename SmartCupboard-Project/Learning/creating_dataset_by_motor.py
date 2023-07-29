# Importing Libraries
import serial
import cv2
import os
import numpy as np
import time
import requests
import tensorflow as tf

main_path = '/home/marios/Desktop/smart_git/SmartCupboard_569/ObjectDetection/dataset_after_demo'  # Path to save the captured picture
path_to_save_cropped_images = '/home/marios/PycharmProjects/ObjectDetection/lazer_detect/cropped'

path_localizer = '/home/marios/Downloads/object_detection_mobile_object_localizer_v1_1_default_1.tflite'

img_height_localizer = 192
img_width_localizer = 192
localizer_threshold = 0.75

request_framesize = requests.get("http://localhost:8080/control?var=framesize&val=6") # Problem --> get dark image
time.sleep(3) # Wait some seconds SO not to get a dark image

port = '/dev/ttyUSB0'

arduino = serial.Serial(port=port, baudrate=2000000, timeout=60)

def write_read(x,y):
    arduino.read(arduino.inWaiting())
    arduino.write(bytes(str(x), 'utf-8'))
    arduino.write(bytes(" ", 'utf-8'))

    arduino.write(bytes(str(y), 'utf-8'))
    arduino.write(bytes("\n", 'utf-8'))

    data = arduino.readline()
    return data

product_name = input('Enter the product name:')
if not os.path.exists(os.path.join(main_path,product_name)):
    os.makedirs(os.path.join(main_path,product_name))

counter_run = 41 # initialize
time.sleep(10)
num_x_init = 0
num_y_init = 80
value = write_read(num_x_init,num_y_init)

for currentX in range(num_x_init,330,5):

    write_read(currentX, num_y_init) # move the camera

    #Take a picture
    request_capture = requests.get("http://localhost:8080/capture")
    filename = 'foto.jpg'  # filename of the picture

    # Save the file of the picture
    f = open(os.path.join(main_path,filename), 'wb')
    f.write(request_capture.content)
    f.close()

    #Rotate and save again
    img = cv2.imread(os.path.join(main_path,filename))
    rotated_img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE) # clockwise
    cv2.imwrite(os.path.join(main_path,filename),rotated_img)

    original_height = rotated_img.shape[0]
    original_width = rotated_img.shape[1]

    #Load localizer
    interpreter = tf.lite.Interpreter(model_path=path_localizer)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.allocate_tensors()

    img_localizer = cv2.resize(rotated_img,(img_width_localizer,img_height_localizer))
    interpreter.set_tensor(input_details[0]['index'],[img_localizer])

    interpreter.invoke() # Run localizer

    detection_boxes = interpreter.get_tensor(output_details[0]["index"])
    detection_scores = interpreter.get_tensor(output_details[2]["index"])

    my_boxes = np.empty((0,4))
    for index, score in enumerate(detection_scores[0]):
        if score > localizer_threshold:
            counter_run += 1
            rectangular = np.reshape(detection_boxes[0][index],(1,4)) # reshape (4,) to (1,4)
            my_boxes = np.append(my_boxes,rectangular,axis=0)
            break

    num_boxes = my_boxes.shape[0]

    for box in range(0,num_boxes):
        # Get the x,y coordinates
        y_min = int(max(1, (my_boxes[box][0] * original_height)))
        x_min = int(max(1, (my_boxes[box][1] * original_width)))
        y_max = int(min(original_height, (my_boxes[box][2] * original_height)))
        x_max = int(min(original_width, (my_boxes[box][3] * original_width)))

        crop_image = rotated_img[y_min:y_max, x_min:x_max]
        cv2.imwrite(os.path.join(main_path,product_name,'foto'+str(counter_run) + '.jpg'),crop_image)

print('end of script')
