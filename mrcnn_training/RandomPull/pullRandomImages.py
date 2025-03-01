import argparse
from ast import arg, walk
import enum
from genericpath import isdir
import os
import json
import random
import shutil

parser = argparse.ArgumentParser(
        description='Mask R-CNN infrence for organoid counting and segmentation')
parser.add_argument('--input', help='Path to input directory', action="append",nargs='+')
parser.add_argument('--out', help='Path to output directory')
parser.add_argument('--count', help='how many random images to pull')
args = parser.parse_args()
assert args.input is not None, "Please provide an input directory"
assert args.out is not None, "Please provide an output directory"
input_directories = args.input
save_directory = args.out

if not os.path.exists(save_directory):
    os.makedirs(save_directory)
input("!!!Warning!!! this action will CLEAR the output directory. Press any key to continue or Ctrl-C to cancel")
# delete all files in output dir

    
for file in os.listdir(save_directory):
    file_path = os.path.join(save_directory, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

# list all files in input directory
counter = 0
def walkDirectory(input_directory):
    global counter
    paths_to_copy = []
    NanoparticleC = os.listdir(input_directory)
    for DirName in NanoparticleC:
        print("walking subdirectory: " + DirName)
        dirPath = os.path.join(input_directory, DirName)
        if isdir(dirPath):

            
        
            randomImages = random.sample(os.listdir(dirPath), int(args.count))
            
            for index, filename in enumerate(randomImages):
                print("copying file: " + filename)
                img_path = os.path.join(input_directory,dirPath, filename)
                paths_to_copy.append(img_path)
                counter += 1

    return paths_to_copy


allPathsToCopy = []

for directory in input_directories:
    directory = directory[0]
    print("opening: " + directory)
    if os.path.isdir(directory):
        paths_to_copy = walkDirectory(directory)
        allPathsToCopy.extend(paths_to_copy)

#shuffle allPathsToCopy
random.shuffle(allPathsToCopy)




mappings = {}
for path in allPathsToCopy:
    #anynomize save name
    save_name = allPathsToCopy.index(path)
    #pad save name with 0's
    save_name = str(save_name).zfill(3)
    save_name = "image_" + str(save_name) + ".png"
    shutil.copy(os.path.join(path), os.path.join(save_directory, save_name))
    if os.name == "nt":
        mappings[save_name] = "".join(path.split("\\")[-2:])
    else:
        mappings[save_name] = "".join(path.split("/")[-2:])
# make a csv from mappings
with open(os.path.join(save_directory, "mappings.csv"), "w") as f:
    for key, value in mappings.items():
        f.write(f"{key},{value}\n")
with open(os.path.join(save_directory, "mappings.json"), "w") as f:
    f.write(json.dumps(mappings))