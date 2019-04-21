#!/usr/bin/env python3
import subprocess
import sys

if __name__ == "__main__":
    print("generating llvm...")
    output = subprocess.call(
        ["python3 source/main.py {0} {1}".format(str(sys.argv[1]), str(sys.argv[2]))],
        shell=True
    )
    print("done")
