# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Activation, Dropout
from keras import optimizers
from keras.utils import plot_model
# Initialising the CNN
classifier = Sequential()
classifier.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(64, 64, 1)))
classifier.add(Conv2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Dropout(0.25))
 
classifier.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Dropout(0.25))
 
classifier.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Dropout(0.25))
 
classifier.add(Flatten())
classifier.add(Dense(512, activation='relu'))
classifier.add(Dropout(0.5))
classifier.add(Dense(4, activation='softmax'))

# Step 3 - Flattening


# Compiling the CNN
optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
classifier.compile(optimizer='rmsprop', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale = 1./255,
shear_range = 0.2,
zoom_range = 0.2,
horizontal_flip = False)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_set = train_datagen.flow_from_directory('resources/neuron/training',
target_size = (64, 64),
color_mode='grayscale',
batch_size = 64,
class_mode = 'categorical')
test_set = test_datagen.flow_from_directory('resources/neuron/test',
target_size = (64, 64),
color_mode='grayscale',
batch_size = 64,
class_mode = 'categorical')
classifier.fit_generator(training_set,
steps_per_epoch = 137,
epochs = 10,
validation_data = test_set,
validation_steps = 36)

# Part 3 - Making new predictions
import numpy as np
from keras.preprocessing import image
test_image = image.load_img('resources/municipal1.png', target_size = (64, 64), grayscale=True)
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
training_set.class_indices

classifier.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
plot_model(classifier, to_file='model.png')
del classifier

if result[0][0] == 1:
	prediction = 'plastic'
else:
	prediction = 'mixed'
	
print(prediction)