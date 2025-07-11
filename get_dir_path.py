import os
cwd = os.getcwd()



#this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(cwd, "data", "data.txt")
print(open(DATA_PATH).read())