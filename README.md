# Photonpacket
Photonpacket is used to analyze photon data.

# Documentation
See documentation at the [FUW server](https://www.fuw.edu.pl/~mparniak/photonpacket/).

To generate documentation go to `doc` and run `./apidoc.sh`. Then run `make html`. The documentation is created in `doc/build/index.html`.

# Installation
You need [Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/pl/downloads/#build-tools-for-visual-studio-2019) (C++ Build Tools) to compile the Cython extensions.

To install in development mode:

    $ pip install -e .