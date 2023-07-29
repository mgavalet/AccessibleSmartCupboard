import matplotlib.pyplot as plt
import time
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# Get the time that code exectution starts
start_time = time.time()

data_dir = '/home/marios/Desktop/smart_git/SmartCupboard_569/ObjectDetection/dataset_after_demo'

# General parameters
batch_size = 5
img_height = 500
img_width = 300
# num_classes = 6
num_classes = 12
epochs = 15

# Load train and validation data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size,
  shuffle=True)

# print(type(train_ds)) # class 'tensorflow.python.data.ops.dataset_ops.BatchDataset

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size,
  shuffle=True)

class_names = train_ds.class_names
print(class_names)


# Build model
model = Sequential([
  # data_augmentation,
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.4),
  layers.Flatten(),
  layers.Dense(64, activation='relu'),
  layers.Dense(num_classes) # no activation
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

# Train
history = model.fit(train_ds, validation_data=val_ds,epochs=epochs,verbose=1)

# Visualize train results
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


# Save the trained model
model.save('afterDemo_12products.h5')

# Print execution time
print("--- %s minutes ---" % ((time.time() - start_time)/60))
