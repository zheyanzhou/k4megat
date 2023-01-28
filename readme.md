k4megat
===
This is a prototype software for the simulation, reconstruction and analysis tasks of **Megat** experiment.
It's built upon [Gaudi](https://github.com/key4hep/Gaudi) framework using [Key4hep](https://github.com/key4hep/) components.

Major dependence
===
  * **Framework**: Gaudi
  * **Detector geometry**: [ DD4hep ](https://dd4hep.web.cern.ch/)
  * **Data model**: EDM4hep
  * **Event Store**: k4FWCore
  * **Simulation driver (Geant4)**: DDG4 or k4SimGeant4 (a hard integration into **k4megat** as _sim_ package, see [sim](doc/sim.org))

Installation
===
The official installation is based on [cvmfs](https://cernvm.cern.ch/fs/) using the software stack of
key4hep. _cvmfs_ client is already deployed in USTC server as well as [the stack of key4hep](https://key4hep.github.io/key4hep-doc/).
The following installation steps are only applicable to the USTC server, which is based on CentOS-7.
For installation in other OS, see [_development_](#development) section.

Step 1: setup build environment
---
After login the USTC servre:
```shell
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

More details about key4hep software stack, check [key4hep official documentation](https://key4hep.github.io/key4hep-doc/setup-and-getting-started/README.html).

Step 2: download the source
---
```shell
git clone https://github.com/MegMev/k4megat
cd k4megat && git checkout -b sim-dev sim-dev
```

Step 3: build & install
---
```shell
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=${your_install_dir} ..
make -j10 install
```

Step 4: setup running environment
---
```shell
source ${your_install_dir}/bin/thismegat_only.sh
```

NOTE:
In case of fresh login after installation, both [Step 1](#Step-1) and [Step 2](#Step-2) need to be repeated to configure the running environment. The two scripts can be put into your shell's login script for convenience.

Step 5: run a test scripts to confirm the installation
---
```shell
cd ../sim/scripts/gaudi
k4run test_sim.py
```
There will be no _ERROR_ message and a ROOT file named "megat.gaudi.root" will be created if the installation is successful.


Development
===
TODO

A light-weight development environment is needed for developers to easily setup a local working copy in 
their own machine. Possible solution:
  * spack
  * lcgcmake

Documentation
===
Most doc files are in [ Org-mode ](https://orgmode.org/) format, saved under [doc](doc).