import os
import random
import string
from captcha_generator_functions import create_CAPTCHA

OUTPUT_DIR = "captcha_dataset"
TRAIN_DIR = os.path.join(OUTPUT_DIR, "train")
VAL_DIR = os.path.join(OUTPUT_DIR, "val")
TEST_DIR = os.path.join(OUTPUT_DIR, "test")
LABELS_FILE_TRAIN = os.path.join(TRAIN_DIR, "labels.csv")
LABELS_FILE_VAL = os.path.join(VAL_DIR, "labels.csv")
LABELS_FILE_TEST = os.path.join(TEST_DIR, "labels.csv")

FONTS_DIR = "captcha_generator/fonts_directory"

IMAGE_WIDTH = 200 #image size
IMAGE_HEIGHT = 80
TEXT_LENGTH_MIN = 4
TEXT_LENGTH_MAX = 6
FONT_SIZE_MIN = 28
FONT_SIZE_MAX = 38

CHARACTERS = string.ascii_letters + string.digits #maj and min letters dans digits inside the Captcha

NUM_TRAIN_IMAGES = 1000 # number of image for training set
NUM_TEST_IMAGES = 200
NUM_VAL_IMAGES = NUM_TEST_IMAGES

def generate_dataset(output_dir, train_dir, val_dir, test_dir, NUM_TRAIN_IMAGES, NUM_VAL_IMAGES, NUM_TEST_IMAGES, image_width, image_height, text_length_min, text_length_max, font_size_min, font_size_max, font_directory):
  for dir_path in [output_dir, train_dir, val_dir, test_dir]:
    os.makedirs(dir_path, exist_ok=True)

  with open(LABELS_FILE_TRAIN, "w") as f_train, open(LABELS_FILE_VAL, "w") as f_val, open(LABELS_FILE_TEST, "w") as f_test:

    header = "filename,text\n"
    f_train.write(header)
    f_val.write(header)
    f_test.write(header)

    print("Generation of the train dataset")
    for i in range(NUM_TRAIN_IMAGES):
      image, text = create_CAPTCHA(image_width, image_height, font_size_min, font_size_max, text_length_min, text_length_max, font_directory)
      filename = f"train_{i}.png"
      image.save(os.path.join(train_dir, filename))
      f_train.write(f"{filename},{text}\n")
      if (i+1) % 100 == 0:
        print(f"{i+1}/{NUM_TRAIN_IMAGES} images generated")


    print("Generation of the validation dataset")
    for i in range(NUM_VAL_IMAGES):
      image, text = create_CAPTCHA(image_width, image_height, font_size_min, font_size_max, text_length_min, text_length_max, font_directory)
      filename = f"val_{i}.png"
      image.save(os.path.join(val_dir, filename))
      f_train.write(f"{filename},{text}\n")
      if (i+1) % 50 == 0:
        print(f"{i+1}/{NUM_VAL_IMAGES} images generated")

    print("Generation of the test dataset")
    for i in range(NUM_VAL_IMAGES):
      image, text = create_CAPTCHA(image_width, image_height, font_size_min, font_size_max, text_length_min, text_length_max, font_directory)
      filename = f"test_{i}.png"
      image.save(os.path.join(test_dir, filename))
      f_train.write(f"{filename},{text}\n")
      if (i+1) % 50 == 0:
        print(f"{i+1}/{NUM_TEST_IMAGES} images generated")


  print("dataset generated")

generate_dataset(OUTPUT_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR, NUM_TRAIN_IMAGES, NUM_VAL_IMAGES, NUM_TEST_IMAGES, IMAGE_WIDTH, IMAGE_HEIGHT, TEXT_LENGTH_MIN, TEXT_LENGTH_MAX, FONT_SIZE_MIN, FONT_SIZE_MAX, FONTS_DIR)
