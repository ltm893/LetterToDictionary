import os
import sys

cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, "LetterToDictionary"))

print(os.getcwd())
print(sys.path)