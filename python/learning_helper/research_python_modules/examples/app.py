# app.py — the script that uses the greet module.
# Run with: python app.py

import greet                # 1) bind the module itself
from greet import greet     # 2) pull one name into our namespace directly

print(greet.greet("Ada"))   # use the module attribute (form 1)
print(greet("Ada"))         # use the imported function (form 2)
print("module name is:", greet.__name__)