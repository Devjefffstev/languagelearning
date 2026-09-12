# main.py — starter for Exercise 02.
# Goal: print sys.path, write a module to a fresh directory,
# extend sys.path, import the module, and prove the import worked.

import sys
import pathlib


def main():
    # TODO 1: print the current contents of sys.path, one entry per line.
    # print(sys.path)
    for path in sys.path: 
        print(path)
    # TODO 2: pick a directory not on sys.path (e.g. /tmp/mods_demo)
    #         and make sure it exists using pathlib.Path.mkdir(...).
    
    str_path="/tmp/code"
    # Create a Path object for the directory
    path = pathlib.Path(str_path)

    # Call mkdir on that Path instance
    path.mkdir(parents=True, exist_ok=True)

    # TODO 3: write a file at <that_dir>/hidden.py that defines
    #         `def ping(): return "pong from <absolute-path-of-hidden.py>"`.
    #         (Use pathlib.Path.write_text.)
    path.write_text(f"{path}/hidden.py",
                   "def ping(): return "pong from {__file__}"")
    # TODO 4: append that directory to sys.path with sys.path.append(...).
    sys.path.append(str_path)
    # TODO 5: import hidden and call hidden.ping(); print the result.
    ## help me here
    # TODO 6: print hidden.__file__ and hidden.__name__ to confirm the import.
    pass


if __name__ == "__main__":
    main()