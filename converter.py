import os

# Paths splitted by semicolon
allPaths = "./demo_libraries/library1;./demo_libraries/library2"


def scanLibraries():
    paths = allPaths.split(';')

    for library in paths:
        print("Library: %s" % library)


scanLibraries()
