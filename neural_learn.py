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
classifier.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(64, 64, 3)))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Conv2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))


classifier.add(Flatten())
classifier.add(Dense(128, activation='relu'))
classifier.add(Dense(4, activation='softmax'))

# Step 3 - Flattening


# Compiling the CNN
op = optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
classifier.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Part 2 - Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=False)
test_datagen = ImageDataGenerator(rescale=1. / 255)
training_set = train_datagen.flow_from_directory('resources/images/train',
                                                 target_size=(64, 64),
                                                 color_mode='rgb',
                                                 batch_size=64,
                                                 class_mode='categorical')
test_set = test_datagen.flow_from_directory('resources/images/test',
                                            target_size=(64, 64),
                                            color_mode='rgb',
                                            batch_size=64,
                                            class_mode='categorical')
classifier.fit_generator(training_set,
                         steps_per_epoch=1841,
                         epochs=5,
                         validation_data=test_set,
                         validation_steps=36)

# Part 3 - Making new predictions


classifier.save('kek.h5')  # creates a HDF5 file 'my_model.h5'
plot_model(classifier, to_file='model.png')
