Hi 
This is my honest coding about Python. I'm not new at coding 

1. The python language reference 
Describe the core semantics of the language https://docs.python.org/3/reference/index.html. THis is like the rules 
 
2. The python standard library 
This is the library reference manual https://docs.python.org/3/library/index.html#library-index. this is like the implementation 


Official Tutorial 
https://docs.python.org/3/tutorial/index.html 

I've been following this tutorial to learn from the basic the complex scenarios 
There is an agent that stores examples and exersices on learning_helper folder that I will be using to reinforce what I just learnt. 

FastAPI 
https://fastapi.tiangolo.com/tutorial/first-steps/

In parallel I've been learning agents on langGraph and ADK, so I want to extend my knowledge on python to there 


--- 
31-08-2026

I learnt: 

FastAPI has an official Vs Code extension 
I added the example and ran it succesfully 
How to install uv environment using uv. i.e uv init my-project --bare, then downloading the fastapi installation uv add "fastapi[standard]" 
Also i left an example of the get [here](python/fastApi/init-project/init-project.py) 
the *.toml file contains the dependencies of my project 
if you open http://localhost:8000/docs you will the openapi docs with Swagger 

you need to be carefull with the folder structure because it will define the the way you define your entrypoint 
so, if the structure looks like this 
.
├── backend
│   ├── main.py
│   ├── __init__.py

you should write on the *toml file 

[tool.fastapi]
entrypoint = "backend.main:app"

---
01-09-2026

this is call a decorator in python 

@app.get("/")

@app.post()
@app.put()
@app.delete()
And the more exotic ones:

@app.options()
@app.head()
@app.patch()
@app.trace()

You can only use await inside of funtions created with async def 
https://fastapi.tiangolo.com/async/
ie. 
@app.get('/')
async def read_results():
    results = await some_library() <--- this is the example 
    return results

Also i leanrt about the billing of FastApiCloud https://fastapicloud.com/docs/team-management/billing/

Hobby and Pro 

Hobby includes 3 pps, 1 custom domain and 0.1 vcpu /512 mb 
What is an app in fastApicloud? 
A FastApi app, so you can build it and deploy it using GitHub workflow actions https://fastapicloud.com/docs/builds-and-deployments/frontend/#deploy-from-ci

I learnt there si a way to run a full stack app 
https://fastapicloud.com/docs/builds-and-deployments/frontend/#build-the-frontend-before-deploying

you just need to build your app and upload the dist/ folder 

I learnt how to use the interactive mode using python from the terminal and understandign the wording needed to run a simple task, and i think it is really usefull if you only have the terminal to interact with 

>>> 2+2+3
7 
If you want to take the last value, use _
>>> 5+_
12
>>> _-4
8

single quotes ('...') or double quotes ("...") with the same result.

String literals can span multiple lines. One way is using triple-quotes: """...""" or '''...'''. End-of-line characters are automatically included in the string, but it’s possible to prevent this by adding a \ at the end of the line. In the following example, the initial newline is not included:

print("""\
... Usage: thingy blabla
... """)

---

03-09-2026

fibonnaci series: 
the sum of two elements defines the next 

a,b = 0,1 
while a < 0
    print(a)
    a,b = b, a+b

Today i want to explore modules and packages. i think it's very important to learn about how to structere your project 

the filename is the module name with the suffix .py appended

from fibo import fib, fibo_array
from fibo import *  <-- this imports all names except those beginning with a underscore 

import fibo as xyz 
xyz.fib(500)

Packages https://docs.python.org/3/tutorial/modules.html#packages
are a way of structuring Python's module namespace by using "dotted module names"
i.e module A.B designates a submodule named B in a package named A 

__init__.py files are required to make python treat dirs containing the files as packages (unless using a namepace package)

Note 
when using 'from package import item'
    item: can be either a submodule or subpackage of the package, or some other named defined in the package, like a function, class or variables

When using: import item.subitem.subsubitem each item except for the last must be a package 

Pending to go deep on __all__ use on __init__.py file 

 Intra-package References
When packages are structured into subpackages (as with the sound package in the example), you can use absolute imports to refer to submodules of siblings packages. For example, if the module sound.filters.vocoder needs to use the echo module in the sound.effects package, it can use from sound.effects import echo.