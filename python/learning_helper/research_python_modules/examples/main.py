# main.py — uses the mymath package.
# Run from the directory containing `mymath/` and `main.py`.

# Three equivalent ways to reach the same function:

# 1) Absolute import, full dotted path
from mymath.stats.basic import mean
print("mean([1,2,3,4]) =", mean([1, 2, 3, 4]))

# 2) Absolute import, shorter form (because mymath/__init__.py re-exports mean)
from mymath import mean as avg
print("avg([10, 20, 30]) =", avg([10, 20, 30]))

# 3) Importing the package and reaching in via attribute
import mymath
print("mymath.add(2, 3) =", mymath.add(2, 3))
print("mymath.multiply(4, 5) =", mymath.multiply(4, 5))
print("mymath.VERSION =", mymath.VERSION)