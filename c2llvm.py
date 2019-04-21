#!/usr/bin/env python3
import subprocess
import sys
import os
sys.path.insert(0, 'source/')
import source.main


def test():
    path = "C_files"
    res_dir = "test_results"
    if not os.path.exists(res_dir):
        os.mkdir('test_results')

    for file in os.listdir(path):
        strip_name = file[0:-2]

        test_dir = "{0}/{1}".format(res_dir, strip_name)
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)

        llvm_name = "{0}.llvm".format(strip_name)
        log_name = "{0}.log".format(strip_name)
        file_l = open("{0}/{1}".format(test_dir, log_name), 'w+')
        sys.stdout = file_l

        dot_name = "{0}.dot".format(strip_name)
        full_dot = "{0}/{1}".format(test_dir, dot_name)
        try:
            source.main.main(["{0}/{1}".format(path, file), "{0}/{1}".format(test_dir, llvm_name), full_dot])
        except:
            pass


if __name__ == "__main__":

    if sys.argv[1] == 'test':
        test()

    else:
        output = subprocess.check_output(
            ["python3","source/main.py", str(sys.argv[1]), str(sys.argv[2])]
        )

