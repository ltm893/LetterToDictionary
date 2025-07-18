from pathlib import Path
import sys


database_module_path =  Path(__file__).resolve().parent.parent / "database" 

print(database_module_path)
sys.path.insert(0, str(database_module_path )) 
print(sys.path)
