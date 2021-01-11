import argparse

"""
Preprocessor:
This python script is to preprocess the given data by augmenting and renaming the file for training.
-i, --img_dir       : Provide path to the folder where the image is stored
-a, --augment       : Provide Boolean value whether to augment the data or not
-n, --rename        : Provide Boolean value whether to rename the data or njot
-rp, --renamepath   : Provide path to the folder where the image to be renamed is stored
-rv, --rename_val   : Provide starting numerical value of the name of the renamed image,
                      File will be renamed in the appending order of the number inputed
                      
Example:
python preprocessor.py -i [PATH_TO_IMAGE] -a [True/False] -n [True/False] -rp [PATH_TO_IMAGE] -rv [Number]
"""

parser = argparse.ArgumentParser(
    description="Data Preprocessor with Augmentation and Renaming macro"
)
parser.add_argument(
    "-i", "--img_dir",
    help = "Path to the folder where image is stored",
    type=str, default=""
)
parser.add_argument(
    "-a", "--augment",
    help = "whether to augment the image",
    type=bool, default=False
)
parser.add_argument(
    "-n", "--rename",
    help = "rename?",
    type=bool, default=False
)
parser.add_argument(
    "-rp", "--renamepath",
    help = "rename?",
    type=str, default=""
)
parser.add_argument(
    "-rv", "--rename_val",
    help = "rename the image file starting from [entered number]",
    type=int, default=1
)

args = parser.parse_args()
DEST = args.img_dir
AUGMENT = args.augment
REDEST = args.renamepath
RENAME = args.rename
RENAME_val= args.rename_val

if AUGMENT is True:
    import Augmentor
    import random
    p = Augmentor.Pipeline(DEST)
    p.greyscale(0.2)
    p.skew_left_right(0.5, 0.2)
    p.skew_top_bottom(0.5, 0.2)
    p.sample(500)


if RENAME is True:
    from os import path
    import os
    count = RENAME_val
    for filename in os.listdir(REDEST):
        dtype = filename[-4:]
        name = str(RENAME_val) + dtype
        RENAME_val = RENAME_val + 1
        os.rename(REDEST+"//"+filename, REDEST+"//"+name)
        print(name)
