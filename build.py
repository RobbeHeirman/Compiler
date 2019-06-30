#!/usr/bin/env python3

import subprocess


def main():
    print("Generating files for Grammars/C4.g4...")

    subprocess.call(
        [
            'java',
            '-jar',
            'antlr.jar',
            '-o',
            'source/gen',
            '-Xexact-output-dir',
            '-Dlanguage=Python3',
            'Grammars/C.g4',
            '-listener'
        ]
    )

    print("Done")


if __name__ == "__main__":
    main()
