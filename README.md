k4megat
===
This is the software for the simulation, reconstruction and analysis tasks of **Megat** experiment.
Component/add-on programming model is adopted for agile development and flexible configuration.

**Megat** is a space gamma-ray telescope proposed by University of Science and Technology of China (USTC).
It aims to discover unknown space sources by focusing on the detection of gamma-rays in the MeV-energy range.
The detector is composed of a time projection chamber in the center for 3D tracking and a CdZnTe calorimeter surrounding it for high-resolution energy measurement.

To view the current detector setup, visit the demo [event display site](https://ufan.site:444/phoenix/#/megat).

Dependency
===

**k4megat** is built upon the latest progress in HENP software community by adopting [Key4hep](https://github.com/key4hep/) components and other modern packages (aka. packages leveraging Modern C++ features):

  * **Geometry description**: [ DD4hep ](https://dd4hep.web.cern.ch/)
  * **Event data model**: [EDM4hep](https://github.com/key4hep/EDM4hep)
  * **Event data store**: [k4FWCore](https://github.com/key4hep/k4FWCore)
  * **Data processing framework**: [Gaudi](https://github.com/key4hep/Gaudi)
  * **Simulation engine (Geant4)**: DDG4 or k4SimGeant4 (a hard integration into **k4megat** as _sim_ package, see [sim](doc/sim.md))

[This document](doc/arch.md) gives a short list of the reasons choosing these building packages instead of [REST-for-Physics](https://github.com/rest-for-physics/).

Installation
===
The official installation is based on [cvmfs](https://cernvm.cern.ch/fs) using the software stack of
key4hep.
This is the recommended way for average developers to quickly start his own development without worrying issues like package dependencies.

**cvmfs** client is already deployed in USTC server as well as [Key4hep](https://key4hep.github.io/key4hep-doc/).
The following installation steps are only applicable to the USTC server, which is based on CentOS-7.

Step 1: setup build environment
---
After login the USTC servre:
```shell
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

More details about key4hep software stack, check [key4hep official documentation](https://key4hep.github.io/key4hep-doc/setup-and-getting-started/README.html).

Step 2: download the source
---
Currently, all developments are pushed to _sim-dev_ branch.

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

The event number can be configured with parameter `EvtMax` in the script. The default value is `1`.

Development
===

Read the [contribution guide](doc/contrib_guide.md) before submitting a pull request.
For novice user of git-based workflow, the guide also gives a short description of necessary steps and useful commands.

The project is still in its early stage.
Many important features are missing, which are listed [here](TODO.md).

Documentation
===
Doxgen-based class references can be generated by:
```shell
# in your build directory
make doc
```
The htmls can be found under `${your_build_dir}/doc/doxgen`

The [doc](doc) directory hosts some OrgMode file, mainly describing the software design and developing guidance.

A more detailed user guide is hosted on [https://k4megat-doc.readthedocs.io](https://k4megat-doc.readthedocs.io)

For curious developers who wanna know more about the building blocks, notes about Gaudi, DD4hep and EDM4hep can be found [https://k4megat-doc.readthedocs.io/projects/third-party](https://k4megat-doc.readthedocs.io/projects/third-party).

