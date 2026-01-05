# runtime-deployment

> Jarvis-cd is a unified platform for deploying various applications

## Repository Info

- **Stars:** 11
- **Forks:** 3
- **Language:** Python
- **License:** Other
- **Topics:** ai4hpc
- **Source:** `https://github.com/iowarp/runtime-deployment`
- **Branch:** `main`
- **Commit:** `d4189d381a1f`
- **Last Commit:** 2026-01-05 13:31:30 -0600
- **Commits:** 1
- **Extracted:** 2026-01-05T14:36:07.335200


## Directory Structure

```
runtime-deployment/
├── .claude/
│   └── agents/
│       ├── code-documenter.md
│       ├── docker-python-test-expert.md
│       ├── git-expert.md
│       ├── jarvis-pipeline-builder.md
│       └── python-code-updater.md
├── .github/
│   └── workflows/
│       ├── build-containers.yaml
│       └── main.yml
├── .vscode/
│   └── launch.json
├── ai-prompts/
│   ├── docker/
│   │   └── phase1.md
│   ├── new-pipeline.md
│   ├── phase-14-update.md
│   ├── phase1-argparse.md
│   ├── phase10-pipeline-index.md
│   ├── phase11-template.md
│   ├── phase12-pipeline.md
│   ├── phase13-jarvis-mod
│   ├── phase14-jarvis-ppl-pkg.md
│   ├── phase15-containers.md
│   ├── phase16-installer.md
│   ├── phase2-hostfile.md
│   ├── phase2-logging.md
│   ├── phase3-launch.md
│   ├── phase4-resource-graph.md
│   ├── phase5-jarvis-repos.md
│   ├── phase6-jarvis-env.md
│   ├── phase8-paths.md
│   └── phase9-pipeline-scripts.md
├── bin/
│   ├── example.slurm
│   ├── jarvis
│   ├── jarvis-imports
│   └── jarvis_resource_graph
├── builtin/
│   ├── builtin/
│   │   ├── adios2_gray_scott/
│   │   │   ├── config/
│   │   │   ├── INSTALL.md
│   │   │   ├── pkg.py
│   │   │   ├── README.md
│   │   │   └── USE.md
│   │   ├── arldm/
│   │   │   ├── example_config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── asan/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── builtin_pkg/
│   │   │   └── package.py
│   │   ├── cm1/
│   │   │   ├── config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── cosmic_tagger/
│   │   │   ├── config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── darshan/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── data_stagein/
│   │   │   └── pkg.py
│   │   ├── ddmd/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── dlio_benchmark/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── echo/
│   │   │   └── pkg.py
│   │   ├── example_app/
│   │   │   └── pkg.py
│   │   ├── example_interceptor/
│   │   │   └── pkg.py
│   │   ├── filebench/
│   │   │   ├── config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── fio/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── gadget2/
│   │   │   ├── config/
│   │   │   ├── paramfiles/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── gadget2_df/
│   │   │   ├── paramfiles/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── gray_scott/
│   │   │   ├── config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── InCompact3D/
│   │   │   ├── config/
│   │   │   ├── spack/
│   │   │   ├── incompact3D.yaml
│   │   │   ├── INSTALL.md
│   │   │   ├── pkg.py
│   │   │   ├── README.md
│   │   │   └── USE.md
│   │   ├── InCompact3D_post/
│   │   │   ├── config/
│   │   │   ├── incompact3d_post.yaml
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── ior/
│   │   │   ├── __init__.py
│   │   │   ├── container.py
│   │   │   ├── default.py
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── lammps/
│   │   │   ├── config/
│   │   │   ├── INSTALL.md
│   │   │   ├── pkg.py
│   │   │   ├── README.md
│   │   │   └── USE.md
│   │   ├── mkfs/
│   │   │   └── pkg.py
│   │   ├── my_shell/
│   │   │   ├── pkg.py
│   │   │   └── test_scirpt.sh
│   │   ├── nyx_lya/
│   │   │   ├── config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── orangefs/
│   │   │   ├── __init__.py
│   │   │   ├── ares.py
│   │   │   ├── custom_kern.py
│   │   │   ├── Dockerfile
│   │   │   ├── fuse.py
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── paraview/
│   │   │   ├── INSTALL.MD
│   │   │   ├── pkg.py
│   │   │   ├── README.md
│   │   │   ├── server_setup.png
│   │   │   └── USE.MD
│   │   ├── post_wrf/
│   │   │   ├── config/
│   │   │   └── pkg.py
│   │   ├── pyflextrkr/
│   │   │   ├── example_config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── pymonitor/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── redis/
│   │   │   ├── config/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── redis-benchmark/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── spark_cluster/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   ├── test_pkg/
│   │   │   └── package.py
│   │   ├── wrf/
│   │   │   ├── config/
│   │   │   ├── INSTALL.md
│   │   │   ├── pkg.py
│   │   │   ├── README.md
│   │   │   ├── USE.md
│   │   │   └── wrf_workflow.png
│   │   ├── ycsbc/
│   │   │   ├── pkg.py
│   │   │   └── README.md
│   │   └── __init__.py
│   ├── config/
│   │   ├── ares.yaml
│   │   ├── deception.yaml
│   │   └── polaris.yaml
│   ├── pipelines/
│   │   ├── examples/
│   │   │   ├── ior_container_test.yaml
│   │   │   └── ior_podman_test.yaml
│   │   ├── unit_tests/
│   │   │   └── test_interceptor.yaml
│   │   ├── simple_test.yaml
│   │   ├── test_interceptor.yaml
│   │   └── test_simple.yaml
│   ├── resource_graph/
│   │   ├── ares.yaml
│   │   ├── deception.yaml
│   │   ├── delta.yaml
... (truncated)
```

## File Statistics

- **Files Processed:** 50
- **Files Skipped:** 0


## README

# Jarvis-CD

Jarvis-CD is a unified platform for deploying various applications, including storage systems and benchmarks. Many applications have complex configuration spaces and are difficult to deploy across different machines.

## Installation

```bash
cd /path/to/jarvis-cd
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

## Configuration (Build your Jarvis setup)

```bash
jarvis init [CONFIG_DIR] [PRIVATE_DIR] [SHARED_DIR]
```
- CONFIG_DIR: Stores Jarvis metadata for pkgs/pipelines (any path you can access)
- PRIVATE_DIR: Per-machine local data (e.g., OrangeFS state)
- SHARED_DIR: Shared across machines with the same view of data

On a personal machine, these can point to the same directory.

## Hostfile (set target nodes)

The hostfile lists nodes for multi-node pipelines (MPI-style format):

Example:
```text
host-01
host-[02-05]
```

Set the active hostfile:
```bash
jarvis hostfile set /path/to/hostfile
```

After changing the hostfile, update the active pipeline:
```bash
jarvis ppl update
```

## Resource Graph (discover storage)

```bash
jarvis rg build
```

## License

BSD-3-Clause License - see [LICENSE](LICENSE) file for details.

**Copyright (c) 2024, Gnosis Research Center, Illinois Institute of Technology**


## Source Files

### `builtin/builtin/InCompact3D/README.md`

```markdown

# The Xcompact3D(Incompact3D) 

## what is the Incompact3D application?
Xcompact3d is a Fortran-based framework of high-order finite-difference flow solvers dedicated to the study of turbulent flows. Dedicated to Direct and Large Eddy Simulations (DNS/LES) for which the largest turbulent scales are simulated, it can combine the versatility of industrial codes with the accuracy of spectral codes. Its user-friendliness, simplicity, versatility, accuracy, scalability, portability and efficiency makes it an attractive tool for the Computational Fluid Dynamics community.

XCompact3d is currently able to solve the incompressible and low-Mach number variable density Navier-Stokes equations using sixth-order compact finite-difference schemes with a spectral-like accuracy on a monobloc Cartesian mesh.  It was initially designed in France in the mid-90's for serial processors and later converted to HPC systems. It can now be used efficiently on hundreds of thousands CPU cores to investigate turbulence and heat transfer problems thanks to the open-source library 2DECOMP&FFT (a Fortran-based 2D pencil decomposition framework to support building large-scale parallel applications on distributed memory systems using MPI; the library has a Fast Fourier Transform module).
When dealing with incompressible flows, the fractional step method used to advance the simulation in time requires to solve a Poisson equation. This equation is fully solved in spectral space via the use of relevant 3D Fast Fourier transforms (FFTs), allowing the use of any kind of boundary conditions for the velocity field. Using the concept of the modified wavenumber (to allow for operations in the spectral space to have the same accuracy as if they were performed in the physical space), the divergence free condition is ensured up to machine accuracy. The pressure field is staggered from the velocity field by half a mesh to avoid spurious oscillations created by the implicit finite-difference schemes. The modelling of a fixed or moving solid body inside the computational domain is performed with a customised Immersed Boundary Method. It is based on a direct forcing term in the Navier-Stokes equations to ensure a no-slip boundary condition at the wall of the solid body while imposing non-zero velocities inside the solid body to avoid discontinuities on the velocity field. This customised IBM, fully compatible with the 2D domain decomposition and with a possible mesh refinement at the wall, is based on a 1D expansion of the velocity field from fluid regions into solid regions using Lagrange polynomials or spline reconstructions. In order to reach high velocities in a context of LES, it is possible to customise the coefficients of the second derivative schemes (used for the viscous term) to add extra numerical dissipation in the simulation as a substitute of the missing dissipation from the small turbulent scales that are not resolved. 

Xcompact3d is currently being used by many research groups worldwide to study gravity currents, wall-bounded turbulence, wake and jet flows, wind farms and active flow control solutions to mitigate turbulence.  ​

## what this model generate:

### Numerical flow solutions
Xcompact3D produces high-fidelity numerical solutions to the Navier–Stokes equations, including: Velocity fields (u, v, w) in 3D. Pressure fields (p). Scalar fields (e.g., temperature, concentration) if configured. Derived quantities such as vorticity, dissipation rates, or turbulent stresses.

### 3D snapshots and flow visualizations
The solver can output 3D snapshots of flow variables at user-defined intervals.
These snapshots can be used for: Flow visualization (e.g., isosurfaces, slices, contours). Statistical analysis (mean fields, fluctuations). Detailed inspection of turbulent structures.

## Benchmark data and case studies
As demonstrated in the paper, Xcompact3D generates data for well-known CFD test cases, including:

1. Taylor–Green vortex: Transition from laminar to turbulent states.

2. Turbulent channel flow: Wall-bounded turbulence with comparisons to reference data.

3. Flow past a cylinder: Including wake dynamics and vortex shedding.

4. Lock-exchange flow: Variable-density gravity currents.

5. Fractal-generated turbulence: Turbulence control and mixing studies.

6. Wind farm simulations: Detailed turbine wake interactions.

##  Key Input Parameters (Xcompact3d)

| **Parameter**     | **Description**                                            | **Example / Options**                       |
|--------------------|------------------------------------------------------------|--------------------------------------------|
| **p_row, p_col**  | Domain decomposition for parallel computation             | Auto-tune (0), or set to match core layout |
| **nx, ny, nz**   | Number of mesh points per direction                         | E.g., 1024, 1025 (non-periodic)           |
| **xlx, yly, zlz** | Physical domain size (normalized or dimensional)          | E.g., 20D (cylinder case)                 |
| **itype**        | Flow configuration                                        | 0–11 (custom, jet, channel, etc.)         |
| **istret**      | Mesh refinement in Y direction                               | 0: none, 1–3: various center/bottom       |
| **beta**         | Refinement strength parameter                               | Positive values (trial & error tuning)     |
| **iin**           | Initial condition perturbations                            | 0: none, 1: random, 2: fixed seed        |
| **inflow_noise**| Noise amplitude at inflow                                   | 0–0.1 (as % of ref. velocity)           |
| **re**            | Reynolds number                                           | E.g., Re = 1/ν                           |
| **dt**            | Time step size                                            | User-defined, depends on resolution        |
| **ifirst, ilast**| Start and end iteration numbers                            | E.g., 0, 50000                            |
| **numscalar**   | Number of scalar fields                                     | Integer ≥ 0                               |
| **iscalar**     | Enable scalar fields                                        | Auto-set if numscalar > 0                |
| **iibm**        | Immersed Boundary Method                                    | 0: off, 1–3: various methods             |
| **ilmn**       | Low Mach number solver                                      | 0: off, 1: on                            |
| **ilesmod**   | LES model selection                                          | 0: off, 1–4: various models             |
| **nclx1...nclzn** | Boundary conditions per direction                         | 0: periodic, 1: free-slip, 2: Dirichlet |
| **ivisu**       | Enable 3D snapshots output                                 | 1: on                                    |
| **ipost**      | Enable online postprocessing                                 | 1: on                                    |
| **gravx, gravy, gravz** | Gravity vector components                          | E.g., (0, -1, 0)                        |
| **ifilter, C_filter** | Solution filtering controls                         | E.g., 1, 0.5                             |
| **itimescheme** | Time integration scheme                                    | E.g., 3: Adams-Bashforth 3, 5: RK3      |
| **iimplicit** | Y-diffusive term scheme                                     | 0: explicit, 1–2: implicit options      |
| **nu0nu, cnu** | Hyperviscosity/viscosity ratios                            | Default: 4, 0.44                        |
| **ipinter**     | Interpolation scheme                                      | 1–3 (Lele or optimized variants)       |
| **irestart**    | Restart from file                                          | 1: enabled                              |
| **icheckpoint** | Checkpoint file frequency                                 | E.g., every 5000 steps                 |
| **ioutput**    | Output snapshot frequency                                 | E.g., every 500 steps                  |
| **nvisu**      | Snapshot size control                                      | Default: 1                             |
| **initstat**  | Start step for statistics collection                        | E.g., 10000                            |
| **nstat**      | Statistics collection spacing                              | Default: 1                             |
| **sc, ri, uset, cp** | Scalar-related parameters                             | Schmidt, Richardson, settling, init conc.|
| **nclxS1...nclzSn** | Scalar BCs                                            | 0: periodic, 1: no-flux, 2: Dirichlet |
| **scalar_lbound, scalar_ubound** | Scalar bounds                           | E.g., 0, 1                             |
| **sc_even, sc_skew** | Scalar symmetry flags                               | True/False                            |
| **alpha_sc, beta_sc, g_sc** | Scalar wall BC params                         | For implicit solvers                   |
| **Tref**       | Reference temperature for scalar                          | Problem-specific                      |
| **iibmS**    | IBM treatment for scalars                                   | 0: off, 1–3: various modes          |

---
```

### `builtin/builtin/InCompact3D_post/README.md`

```markdown

This is the post-processing to read file with adios2 bp5 from incompact3D examples.

### how to install
Installing the coeus-adapter will also generate an executable file named inCompact3D_analysis

### Jarvis(ADIOS2)

step 1: Build environment
```
spack load incompact3D@coeus
spack load openmpi
export PATH=~/coeus-adapter/build/bin/:$PATH
```
step 3: add jarvis repo
```
jarvis repo add coeus_adapter/test/jarvis/jarvis_coeus
```
step 4: Set up the jarvis packages
```
jarvis ppl create incompact3D_post
jarvis ppl append InCompact3D_post file_location=/path/to/data.bp5 nprocs=16 ppn=16 engine=bp5
jarvis ppl env build
```

step 5: Run with jarvis
```
jarvis ppl run
```

### Jarvis (Hermes)
This is the procedure for running the application with Hermes as the I/O engine.<br>
step 1: Place the run scripts in the example folder and copy an existing script as input.i3d.
The following example demonstrates this setup for the Pipe-Flow benchmark.
```
cd Incompact3d/examples/Pipe-Flow
cp input_DNS_Re1000_LR.i3d input.i3d
```

step 2: Build environment
```
spack load hermes@master
spack load incompact3D@coeus
spack load openmpi
export PATH=/incompact3D/bin:$PATH
export PATH=~/coeus-adapter/build/bin:$PATH
export LD_LIBRARY_PATH=~/coeus-adapter/build/bin:LD_LIBRARY_PATH
```
step 3: add jarvis repo
```
jarvis repo add coeus_adapter/test/jarvis/jarvis_coeus
```
step 4: Set up the jarvis packages
```
jarvis ppl create incompact3d
jarvis ppl append hermes_run provider=sockets
jarvis ppl append Incompact3d example_location=/path/to/incompact3D-coeus engine=hermes nprocs=16 ppn=16 benchmarks=Pipe-Flow
jarvis ppl append InCompact3D_post file_location=/path/to/data.bp5 nprocs=16 ppn=16 engine=hermes
jarvis ppl env build
```

step 5: Run with jarvis
```
jarvis ppl run
```
```

### `builtin/builtin/adios2_gray_scott/README.md`

```markdown
# Gray-Scott Model
## what is the Gray-Scott application?
The Gray-Scott system is a **reaction–diffusion system**, meaning it models a process involving both chemical reactions and diffusion across space. In the case of the Gray-Scott model that reaction is a chemical reaction between two substances 
 u and v, both of which diffuse over time. During the reaction gets used up, while  is produced. The densities of the substances 
 and are represented in the simulation.

## what this model generate:
The Gray-Scott system models the chemical reaction

U + 2V ->  3V

This reaction consumes U and produces V. Therefore, the amount of both substances needs to be controlled to maintain the reaction. This is done by adding U at the "feed rate" F and removing V at the "kill rate" k. The removal of V can also be described by another chemical reaction:

V -> P

For this reaction P is an inert product, meaning it doesn't react and therefore does not contribute to our observations. In this case the Parameter k controls the rate of the second reaction.


## what is the input of gray-scott

The Gray-Scott system models two chemical species:

U: the feed chemical, continuously added to the system.

V: the activator chemical, which is produced during the reaction and also removed.




##  Key Input Parameters

| Parameter      | Description                                    | Typical Range or Example Values         |
|----------------|------------------------------------------------|----------------------------------------|
| **F**          | Feed rate of U (controls how quickly U is replenished in the system) | 0.01 – 0.08         |
| **k**          | Kill rate of V (controls how quickly V is removed from the system) | 0.03 – 0.07         |
| **Du**         | Diffusion coefficient for U                   | Typically ~2 × Dv        |
| **Dv**         | Diffusion coefficient for V                   | Lower than Du (e.g., half) |
| **Grid size(L)**  | Spatial resolution of the simulation grid     | 256×256, 512×512       |
| **Time step(Steps)**  | Time integration step size                   | 0.01 – 1.0            |
| **Initial condition** | Initial distribution of U and V         | U = 1, V = 0 with small localized perturbations (e.g., center patch with V = 1) |
| **Simulation speed** | Controls visual update or iteration speed | 1×, 2×, etc.          |
| **Color scheme** | Display mode for concentration visualization | Black & white or RGB sliders |
| **Noise(noise)** | add noise for the simulation | 0.01~0.1 |
| **I/O frequency(plotgap)** | the frequecey of I/O between simulation steps  | 1~10 |
```

### `builtin/builtin/arldm/README.md`

```markdown
The AR-LDM (Auto-Regressive Latent Diffusion Models) is a latent diffusion model auto-regressively conditioned on history captions and generated images.
See the [official repo](https://github.com/xichenpan/ARLDM) for more detail.

# Table of Content
0. [Dependencies](#0-dependencies)
1. [Installation](#1-installation)
2. [Running ARLDM](#2-running-arldm)
3. [ARLDM with Slurm](#3-arldm-with-slurm)
4. [ARLDM + Hermes](#4-arldm--hermes)
5. [ARLDM on Node Local Storage](#5-arldm-on-node-local-storage)
6. [ARLDM + Hermes on Node Local Storage](#6-arldm--hermes-on-node-local-storage)
7. ARLDM + Hermes with Multinodes Slurm (Not supported)



# 0. Dependencies

## 0.1. conda
- Prepare Conda
Get the miniconda3 installation script and run it
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh.sh
```

## 0.2. jarvis-cd & scspkg
Follow steps here: https://github.com/grc-iit/jarvis-cd


## 0.3. spack
Spack is used to install HDF5, MPICH, and Hermes.
Install spack steps are here: https://spack.readthedocs.io/en/latest/getting_started.html#installation

## 0.4. HDF5 (1.14.0+)
HDF5 is require, (1.14.0+) is required by Hermes and h5py==3.8.0.

Use spack to install hdf5
```bash
spack install hdf5@1.14.0+hl~mpi
```

## 0.5. MPI
Either OpenMPI or MPICH works, this is required by Hermes and mpi4py


Use spack to install mpich
```bash
spack install mpich@3.4.3
```

## 0.6. Installation Tools
You need `wget` and `gdown` to download the datasets online:
- wget
You can install wget either with `apt-get` or `spack`
```bash
sudo apt-get install wget
# or
spack install wget
spack load wget
# check if wget is usable
which wget
```
- gdown
```shell
python3 -m pip install gdown==4.5.1 # or 4.6.0
pip show gdown
```


# 1. Installation

## 1.1 create arldm scs package
```bash
scspkg create arldm
cd `scspkg pkg src arldm`
git clone https://github.com/candiceT233/ARLDM
cd ARLDM
git switch ares # Use the ares branch
export ARLDM_PATH=`scspkg pkg src arldm`/ARLDM
scspkg env set arldm ARLDM_PATH=$ARLDM_PATH HDF5_USE_FILE_LOCKING=FALSE
```


## 1.2 Prepare conda environment and python packages:
```bash
cd `scspkg pkg src arldm`/ARLDM

YOUR_HDF5_DIR="`which h5cc |sed 's/.\{9\}$//'`"
conda env create -f arldm_conda.yaml -n arldm
conda activate arldm
pip uninstall h5py;
HDF5_MPI="OFF" HDF5_DIR=${YOUR_HDF5_DIR} pip install --no-cache-dir --no-binary=h5py h5py==3.8.0
conda deactivate
```



# 2. Running ARLDM

## 2.1.0 Internet Access
Internet access is required when running this program for the first time, you will encounter below error:
```log
  File "/home/$USER/miniconda3/envs/arldm/lib/python3.8/site-packages/transformers/tokenization_utils_base.py", line 1761, in from_pretrained
    raise EnvironmentError(
OSError: Can't load tokenizer for 'runwayml/stable-diffusion-v1-5'. If you were trying to load it from 'https://huggingface.co/models', make sure you don't have a local directory with the same name. Otherwise, make sure 'runwayml/stable-diffusion-v1-5' is the correct path to a directory containing all relevant files for a CLIPTokenizer tokenizer.
```

## 2.1. Setup Environment
Currently setup input path in a shared storage, below is a example on Ares cluster.
Setup experiment input and ouput paths:
```bash
EXPERIMENT_PATH=~/experiments/arldm_run
export EXPERIMENT_INPUT_PATH=$EXPERIMENT_PATH/input_data

scspkg env set arldm EXPERIMENT_INPUT_PATH=$EXPERIMENT_INPUT_PATH

mkdir -p $EXPERIMENT_INPUT_PATH $EXPERIMENT_INPUT_PATH/zippack
```

## 2.2. Download Pretrain Model
The pretrain model is ~ 3.63 GB (~ 10 mins on Ares)
```bash
cd $EXPERIMENT_PATH
conda activate arldm
wget https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large.pth
export PRETRAIN_MODEL_PATH=`realpath model_large.pth`
scspkg env set arldm PRETRAIN_MODEL_PATH=$PRETRAIN_MODEL_PATH
conda deactivate
```

## 2.3. Download Input Data
You should prepare at least one dataset to run the script. There are 4 available datasets for download `vistsis`, `vistdii`, `pororo`, and `flintstones`.

### 2.3.1 VISTSIS and VISTDII

1. Download VISTSIS, original VIST-SIS (~23MB) url links [here](https://visionandlanguage.net/VIST/json_files/story-in-sequence/SIS-with-labels.tar.gz)
```shell
cd $EXPERIMENT_INPUT_PATH
wget https://visionandlanguage.net/VIST/json_files/story-in-sequence/SIS-with-labels.tar.gz
tar -vxf SIS-with-labels.tar.gz
mv sis vistsis # ~ 172M

# save downloaded package to different directory
mv SIS-with-labels.tar.gz $EXPERIMENT_INPUT_PATH/zippack
```

2. Download VISTSIS, original VIST-DII (~18MB) url links [here](https://visionandlanguage.net/VIST/json_files/description-in-isolation/DII-with-labels.tar.gz)
```shell
cd $EXPERIMENT_INPUT_PATH
wget https://visionandlanguage.net/VIST/json_files/description-in-isolation/DII-with-labels.tar.gz
tar -vxf DII-with-labels.tar.gz
mv dii vistdii # ~ 125M

# save downloaded package to different directory
mv DII-with-labels.tar.gz $EXPERIMENT_INPUT_PATH/zippack
```

3. Download the VIST images by running below command (this will take over 2 hours on Ares)
```shell
cd $ARLDM_PATH
conda activate arldm
python data_script/vist_img_download.py --json_dir $EXPERIMENT_INPUT_PATH/vistdii --img_dir $EXPERIMENT_INPUT_PATH/visit_img --num_process 12
```

### 2.3.3 flintstones 
* Original FlintstonesSV dataset [here](https://drive.google.com/file/d/1kG4esNwabJQPWqadSDaugrlF4dRaV33_/view?usp=sharing).
```shell
cd $EXPERIMENT_INPUT_PATH
gdown "1kG4esNwabJQPWqadSDaugrlF4dRaV33_&confirm=t" # ~10 mins on Ares
unzip flintstones_data.zip # 4.9G, ~2 mins on Ares
mv flintstones_data flintstones # 6.6G
mv flintstones_data.zip $EXPERIMENT_INPUT_PATH/zippack
```
<!-- gdown https://drive.google.com/u/0/uc?id=1kG4esNwabJQPWqadSDaugrlF4dRaV33_&export=download -->


### 2.3.2 pororo 
* Original PororoSV dataset [here](https://drive.google.com/file/d/11Io1_BufAayJ1BpdxxV2uJUvCcirbrNc/view?usp=sharing).
```shell
cd $EXPERIMENT_INPUT_PATH
gdown "11Io1_BufAayJ1BpdxxV2uJUvCcirbrNc&confirm=t" # ~30 mins on Ares
unzip pororo.zip # 15GB
mv pororo_png pororo # 17GB
mv pororo.zip $EXPERIMENT_INPUT_PATH/zippack
```
<!-- gdown https://drive.google.com/u/0/uc?id=11Io1_BufAayJ1BpdxxV2uJUvCcirbrNc&export=download -->


## 2.3. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

For details building resource graph, please refer to https://github.com/grc-iit/jarvis-cd/wiki/2.-Resource-Graph.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2.4 Create a Pipeline

The Jarvis pipeline will store all configuration data needed by ARLDM.

```bash
jarvis pipeline create arldm_test
```

## 2.5. Save Environment
Create the environment variables needed by ARLDM.
```bash
spack load hdf5@1.14.0+hl~mpi
module load arldm
```
<!-- conda activate arldm -->

Store the current environment in the pipeline.
```bash
jarvis env build arldm \
+EXPERIMENT_PATH +EXPERIMENT_INPUT_PATH +EXPERIMENT_OUTPUT_PATH \
+ARLDM_PATH +PRETRAIN_MODEL_PATH
jarvis pipeline env copy arldm
```

## 2.6. Add pkgs to the Pipeline
Create a Jarvis pipeline with ARLDM.
```bash
jarvis pipeline append arldm runscript=vistsis
```

## 2.7. Run Experiment

Run the experiment, output are generated in `$EXPERIMENT_INPUT_PATH/output_data`.
```bash
jarvis pipeline run
```

## 2.8. Clean Data

Clean data produced by ARLDM
```bash
jarvis pipeline clean
```



# 3. ARLDM With Slurm

## 3.1 Local Cluster
`ppn` must equal or greater than `num_workers`,which is default to 1.
```bash
jarvis pipeline sbatch job_name=arldm_test nnodes=1 ppn=2 output_file=./arldm_test.out error_file=./arldm_test.err
```

## 3.2 Multi Nodes Cluster (TODO)
ARLDM with jarvis-cd is currently only set to run with single node and using CPU.
    - Multiple CPU worker not tested
    - GPU not tested



# 4. ARLDM + Hermes

## 4.0. Dependencies
### 4.0.1 HDF5
Hermes must compile with HDF5, makesure [download HDF5-1.14.0 with spack](#04-hdf5-1140).

### 4.0.2 Install Hermes dependencies with spack
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
spack install hermes_shm ^hdf5@1.14.0+hl~mpi ^mpich@3.4.3
```

### 4.0.3 Install Hermes with scspkg
1. Option 1: build with POSIX adaptor
```bash
spack load hermes_shm
scspkg create hermes
cd `scspkg pkg src hermes`
git clone https://github.com/HDFGroup/hermes
cd hermes
mkdir build
cd build
cmake ../ -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX=`scspkg pkg root hermes` \
    -DHERMES_MPICH="ON" \
    -DHERMES_ENABLE_POSIX_ADAPTER="ON" \
```

2. Option 2: build with VFD adaptor (This is not working yet)
```bash
spack load hermes_shm
scspkg create hermes
cd `scspkg pkg src hermes`
git clone https://github.com/HDFGroup/hermes
cd hermes
mkdir build
cd build
cmake ../ -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX=`scspkg pkg root hermes` \
    -DHERMES_ENABLE_MPIIO_ADAPTER="ON" \
    -DHERMES_MPICH="ON" \
    -DHERMES_ENABLE_POSIX_ADAPTER="ON" \
    -DHERMES_ENABLE_STDIO_ADAPTER="ON" \
    -DHERMES_ENABLE_VFD="ON" \
```

## 4.1. Setup Environment

Create the environment variables needed by Hermes + ARLDM
```bash
RUN_SCRIPT=vistsis # can change to other datasets
spack load hermes_shm
module load hermes arldm
```

## 4.2. Create a Resource Graph

Same as [above](#2-create-a-resource-graph).

## 4.3. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Hermes
and ARLDM.

```bash
jarvis pipeline create hermes_arldm_test
```

## 4.4. Save Environment

Store the current environment in the pipeline.
```bash
jarvis pipeline env build +PRETRAIN_MODEL_PATH +EXPERIMENT_INPUT_PATH +ARLDM_PATH
```

## 4.5. Add pkgs to the Pipeline

Create a Jarvis pipeline with Hermes, using the Hermes POSIX interceptor.
```bash
jarvis pipeline append hermes_run --sleep=10 include=$EXPERIMENT_INPUT_PATH/${RUN_SCRIPT}_out.h5
jarvis pipeline append hermes_api +posix
jarvis pipeline append arldm runscript=vistsis with_hermes=true
```

## 4.6. Run the Experiment

Run the experiment, output are generated in `$EXPERIMENT_INPUT_PATH/output_data`.
```bash
jarvis pipeline run
```

## 4.7. Clean Data

To clean data produced by Hermes + ARLDM:
```bash
jarvis pipeline clean
```



# 5. ARLDM on Node Local Storage
For cluster that has node local storage, you can stagein data from shared storage, then run arldm.

## 5.1 Setup Environment
Currently setup DEFAULT input path in a shared storage, below is a example on Ares cluster using node local nvme.
```bash
RUN_SCRIPT=vistsis # can change to other datasets
EXPERIMENT_PATH=~/experiments/arldm_run # NFS
SHARED_INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
cd $EXPERIMENT_PATH; export PRETRAIN_MODEL_PATH=`realpath model_large.pth`

LOCAL_EXPERIMENT_PATH=/mnt/nvme/$USER/arldm_run
LOCAL_INPUT_PATH=$LOCAL_EXPERIMENT_PATH/input_data
```

## 5.2. Download Pretrain Model and Input Data
Same as above [download pretrain](#22-download-pretrain-model) and [download input](#23-download-input-data).

## 5.3. Create a Resource Graph
Same as [above](#23-create-a-resource-graph)

## 5.4. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by ARLDM.

```bash
jarvis pipeline create arldm_local
```

## 5.5. Save Environment
Create the environment variables needed by ARLDM.
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
module load arldm
```


Store the current environment in the pipeline.
```bash
jarvis pipeline env build +PRETRAIN_MODEL_PATH +EXPERIMENT_INPUT_PATH +ARLDM_PATH
```


## 5.6. Add pkgs to the Pipeline
Add data_stagein to pipeline before arldm.
- For `RUN_SCRIPT=vistsis` you need to stage in three different input directories:
```bash 
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$SHARED_INPUT_PATH/vistdii,$SHARED_INPUT_PATH/vistsis,$SHARED_INPUT_PATH/visit_img,$PRETRAIN_MODEL_PATH \
mkdir_datapaths=$LOCAL_INPUT_PATH
```

- For other `RUN_SCRIPT`, you only need to stagein one directory:
```bash 
RUN_SCRIPT=pororo
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$SHARED_INPUT_PATH/$RUN_SCRIPT \
mkdir_datapaths=$LOCAL_INPUT_PATH
```


Create a Jarvis pipeline with ARLDM.
```bash
jarvis pipeline append arldm runscript=$RUN_SCRIPT local_exp_dir=$LOCAL_INPUT_PATH
```

## 5.7. Run the Experiment

Run the experiment, output are generated in `$LOCAL_INPUT_PATH/output_data`.
```bash
jarvis pipeline run
```

## 5.8. Clean Data

To clean data produced by Hermes + ARLDM:
```bash
jarvis pipeline clean
```



# 6. ARLDM + Hermes on Node Local Storage
Every step the same as [ARLDM + Hermes](#4-arldm-with-hermes), except for when creating a Jarvis pipeline with Hermes, using the Hermes VFD interceptor:
- Example using `RUN_SCRIPT=vistsis` you need to stage in three different input directories.
```bash
# Setup env
RUN_SCRIPT=vistsis # can change to other datasets
EXPERIMENT_PATH=~/experiments/arldm_run # NFS
SHARED_INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
cd $EXPERIMENT_PATH; export PRETRAIN_MODEL_PATH=`realpath model_large.pth`

LOCAL_EXPERIMENT_PATH=/mnt/nvme/$USER/arldm_run
LOCAL_INPUT_PATH=$LOCAL_EXPERIMENT_PATH/input_data

# add pkg to pipeline
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$SHARED_INPUT_PATH/vistdii,$SHARED_INPUT_PATH/vistsis,$SHARED_INPUT_PATH/visit_img,$PRETRAIN_MODEL_PATH \
mkdir_datapaths=$LOCAL_INPUT_PATH

jarvis pipeline append hermes_run --sleep=10 include=$LOCAL_INPUT_PATH/${RUN_SCRIPT}_out.h5

jarvis pipeline append hermes_api +posix

jarvis pipeline append arldm runscript=vistsis arldm_path="`scspkg pkg src arldm`/ARLDM" with_hermes=true local_exp_dir=$LOCAL_INPUT_PATH
```


# 7. ARLDM + Hermes with Multinodes Slurm (TODO)
Multinodes ARLDM is not supported yet.
```

### `builtin/builtin/asan/README.md`

```markdown
Hermes is a multi-tiered I/O buffering platform. This is module encompasses the
interceptors (MPI-IO, STDIO, POSIX, and VFD) provided in Hermes.

# Installation

```bash
spack install hermes@master
```

```bash
jarvis pipeline create hermes
jarvis pipeline append hermes --sleep=5
jarvis pipeline append hermes_api +posix -mpich
jarvis pipeline run
```
```

### `builtin/builtin/cm1/README.md`

```markdown
CM1 is a simulation code.

# Dependencies

```bash
spack install intel-oneapi-compilers
spack load intel-oneapi-compilers
spack compilers add
spack install h5z-zfp%intel
```

# Compiling / Installing

```bash
git clone git@github.com:lukemartinlogan/cm1r19.8-LOFS.git
cd cm1r19.8-LOFS
# COREX * COREY is the number of cores you intend to use on the system
# They do not need to be 2 and 2 here, but this is how our configurations are compiled for now
COREX=2 COREY=2 bash buildCM1-spack.sh
export PATH=${PWD}/run:${PATH}
export CM1_PATH=${PWD}
```

# Usage

```bash
jarvis pipeline create cm1
jarvis pipeline append cm1 corex=2 corey=2
```
```

### `builtin/builtin/cosmic_tagger/README.md`

```markdown
# Conda
Get the miniconda3 installation script and run it
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

# Cosmic Tagger
[Cosmic Tagger](https://github.com/coreyjadams/CosmicTagger) trains a CNN to separate cosmic pixels.

Conda:
```
conda create -n cosmic_tagger python==3.7
conda activate cosmic_tagger
conda install cmake hdf5 scikit-build numpy
```

Install Larc3
```
git clone https://github.com/DeepLearnPhysics/larcv3.git
cd larcv3
git submodule update --init
pip install -e .
```

Download cosmic tagger
```
git clone https://github.com/coreyjadams/CosmicTagger.git
cd CosmicTagger
pip install -r requirements.txt
```
```

### `builtin/builtin/darshan/README.md`

```markdown
Darshan is an I/O profiling tool. This repo intercepts application I/O and
dumps them into a log that can be parsed to collect metrics such as I/O time.

# Dependencies

# Compiling / Installing

```bash
scspkg create darshan
cd $(scspkg pkg src darshan)
git clone https://github.com/darshan-hpc/darshan.git
cd darshan
git fetch --all --tags --prune
git checkout tags/darshan-3.4.4
./prepare.sh

cd darshan-runtime
./configure --with-log-path=/darshan-logs \
--with-jobid-env=PBS_JOBID \
--with-log-path-by-env=DARSHAN_LOG_DIR \
--prefix=$(scspkg pkg root darshan) \
--enable-hdf5-mod \
CC=mpicc
# --enable-pnetcdf-mod \
make -j32
make install

cd ../darshan-util
./configure \
--prefix=$(scspkg pkg root darshan) \
--enable-pydarshan
make -j32
make install
```

# Usage

Create darshan environment:
```bash
module load darshan
jarvis env build darshan
```

Create a pipeline:
```bash
jarvis pipeline append darshan log_dir=${HOME}/darshan_logs
jarvis pipeline append ior
```

Run the pipeline:
```bash
jarvis pipeline run
```

# Analysis

There are several ways to analyze the output of Darshan:
```
darshan-job-summary.pl ${HOME}/darshan_logs
```
```

### `builtin/builtin/ddmd/README.md`

```markdown
# DeepDriveMD-F (DDMD)
DeepDriveMD: Deep-Learning Driven Adaptive Molecular Simulations (file-based continual learning loop).
See the [official repo](https://github.com/DeepDriveMD/DeepDriveMD-pipeline) for more detail.

# Table of Content
0. [Dependencies](#0-dependencies)
1. [Installation](#1-installation)
2. [Running DDMD](#2-running-ddmd)
3. [DDMD with Slurm](#3-ddmd-with-slurm)
4. [DDMD + Hermes](#4-ddmd--hermes)
5. [DDMD on Node Local Storage (FIXME)](#5-ddmd-on-node-local-storage)
6. [DDMD + Hermes on Node Local Storage (FIXME)](#6-ddmd--hermes-on-node-local-storage)
7. DDMD + Hermes with Multinodes Slurm (TODO)



# 0. Dependencies

## 0.1. conda
- Prepare Conda
Get the miniconda3 installation script and run it
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh.sh
```

## 0.2. jarvis-cd & scspkg
Follow steps here: https://github.com/grc-iit/jarvis-cd


## 0.3. spack
Spack is used to install HDF5, MPICH, and Hermes.
Install spack steps are here: https://spack.readthedocs.io/en/latest/getting_started.html#installation

## 0.4. HDF5 (1.14.0+)
HDF5 is require, (1.14.0+) is required by Hermes and h5py==3.8.0.

Use spack to install hdf5
```bash
spack install hdf5@1.14.0+hl~mpi
```


## 0.5. MPI
Either OpenMPI or MPICH works, this is required by Hermes(VFD depend on MPIIO adaptor)


Use spack to install mpich
```bash
spack install mpich@3.4.3
``` 



# 1. Installation

## 1.1 create ddmd scs package
```bash
scspkg create ddmd
cd `scspkg pkg src ddmd`
git clone https://github.com/candiceT233/deepdrivemd_pnnl.git deepdrivemd
cd deepdrivemd
export DDMD_PATH="`pwd`"
scspkg env set ddmd DDMD_PATH=$DDMD_PATH HDF5_USE_FILE_LOCKING=FALSE
```


## 1.2 Prepare conda environment and python packages
### 1.2.1 Set conda environment variable
```bash
export CONDA_OPENMM=hermes_openmm7_ddmd
export CONDA_PYTORCH=hm_ddmd_pytorch
```


### 1.2.2 Create the respective conda environment with YML files
```bash
cd "`scspkg pkg src ddmd`/deepdrivemd"
conda env create -f ddmd_openmm7.yaml --name=${CONDA_OPENMM}
conda env create -f ddmd_pytorch.yaml --name=${CONDA_PYTORCH}
```



### 1.2.2 Update the conda environment python packages
- for `CONDA_OPENMM`
```bash
cd `scspkg pkg src ddmd`
conda activate $CONDA_OPENMM
export DDMD_PATH="`pwd`"

cd $DDMD_PATH/submodules/MD-tools
pip install -e .

cd $DDMD_PATH/submodules/molecules
pip install -e .

pip uninstall h5py;
HDF5_MPI="OFF" HDF5_DIR=${YOUR_HDF5_DIR} pip install --no-cache-dir --no-binary=h5py h5py==3.8.0

conda deactivate
```


- for `CONDA_PYTORCH`
```bash
cd `scspkg pkg src ddmd`
conda activate $CONDA_PYTORCH
export DDMD_PATH="`pwd`"

cd $DDMD_PATH/submodules/MD-tools
pip install .

cd $DDMD_PATH/submodules/molecules
pip install .

cd $DDMD_PATH
pip install .

pip uninstall h5py;
HDF5_MPI="OFF" HDF5_DIR=${YOUR_HDF5_DIR} pip install --no-cache-dir --no-binary=h5py h5py==3.8.0

conda deactivate
```


# 2. Running DDMD

## 2.1. Setup Environment
Currently setup input path in a shared storage.
Setup experiment input and ouput paths:
```bash
EXPERIMENT_PATH=~/experiments/ddmd_runs #NFS
mkdir -p $EXPERIMENT_PATH
```


## 2.2. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

For details building resource graph, please refer to https://github.com/grc-iit/jarvis-cd/wiki/2.-Resource-Graph.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2.3 Create a Pipeline

The Jarvis pipeline will store all configuration data needed by DDMD.

```bash
jarvis pipeline create ddmd_test
```

## 2.4. Save Environment
Create the environment variables needed by DDMD.
```bash
spack load hdf5@1.14.0+hl~mpi mpich
module load ddmd
```

Store the current environment in the pipeline.
```bash
jarvis pipeline env build +CONDA_OPENMM +CONDA_PYTORCH +DDMD_PATH
```

## 2.5. Add pkgs to the Pipeline
Create a Jarvis pipeline with DDMD.
```bash
jarvis pipeline append ddmd
```

## 2.6. Run Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 2.8. Clean Data

Clean data produced by DDMD
```bash
jarvis pipeline clean
```



# 3. DDMD With Slurm

## 3.1 Local Cluster
`ppn` must equal or greater than `num_workers`,which is default to 1.
```bash
jarvis pipeline sbatch job_name=ddmd_test nnodes=1 ppn=2 output_file=./ddmd_test.out error_file=./ddmd_test.err
```

## 3.2 Multi Nodes Cluster (TODO)
DDMD with jarvis-cd is currently only set to run with single node and using CPU.
    - Multiple CPU worker not tested
    - GPU not tested



# 4. DDMD + Hermes

## 4.0. Dependencies
### 4.0.1 HDF5
Hermes must compile with HDF5, makesure [download HDF5-1.14.0 with spack](#04-hdf5-1140).

### 4.0.2 Install Hermes dependencies with spack
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
spack install hermes_shm ^hdf5@1.14.0+hl~mpi ^mpich@3.4.3
```

### 4.0.3 Install Hermes with scspkg
```bash
spack load hermes_shm
scspkg create hermes
cd `scspkg pkg src hermes`
git clone https://github.com/HDFGroup/hermes
cd hermes
mkdir build
cd build
cmake ../ -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX=`scspkg pkg root hermes` \
    -DHERMES_ENABLE_MPIIO_ADAPTER="ON" \
    -DHERMES_MPICH="ON" \
    -DHERMES_ENABLE_POSIX_ADAPTER="ON" \
    -DHERMES_ENABLE_STDIO_ADAPTER="ON" \
    -DHERMES_ENABLE_VFD="ON" \

```

## 4.1. Setup Environment

Create the environment variables needed by Hermes + DDMD
```bash
spack load hermes_shm
module load hermes ddmd
```

## 4.2. Create a Resource Graph

Same as [above](#2-create-a-resource-graph).

## 4.3. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Hermes
and DDMD.

```bash
jarvis pipeline create hermes_ddmd_test
```

## 4.4. Save Environment

Store the current environment in the pipeline.
```bash
jarvis pipeline env build +CONDA_OPENMM +CONDA_PYTORCH +DDMD_PATH
```

## 4.5. Add pkgs to the Pipeline

Create a Jarvis pipeline with Hermes, using the Hermes VFD interceptor.
```bash
jarvis pipeline append hermes_run --sleep=10 include=$EXPERIMENT_PATH
jarvis pipeline append hermes_api +vfd
jarvis pipeline append ddmd update_envar=true
```

## 4.6. Run the Experiment (TODO)

Run the experiment
```bash
jarvis pipeline run
```

## 4.7. Clean Data

To clean data produced by DDMD:
```bash
jarvis pipeline clean
```



# 5. DDMD on Node Local Storage
For cluster that has node local storage, you can stagein data from shared storage, then run ddmd.

## 5.1 Setup Environment
Currently setup DEFAULT input path in a shared storage, below is a example on Ares cluster using node local nvme.
```bash
RUN_SCRIPT=vistsis # can change to other datasets
EXPERIMENT_PATH=~/experiments/ddmd_run # NFS
INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
cd $EXPERIMENT_PATH; export PRETRAIN_MODEL_PATH=`realpath model_large.pth`

LOCAL_EXPERIMENT_PATH=/mnt/nvme/$USER/ddmd_run
LOCAL_INPUT_PATH=$LOCAL_EXPERIMENT_PATH/input_data
LOCAL_OUTPUT_PATH=$LOCAL_EXPERIMENT_PATH/output_data
```

## 5.2. Download Pretrain Model and Input Data
Same as above [download pretrain](#22-download-pretrain-model) and [download input](#23-download-input-data).

## 5.3. Create a Resource Graph
Same as [above](#23-create-a-resource-graph)

## 5.4. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by DDMD.

```bash
jarvis pipeline create ddmd_local
```

## 5.5. Save Environment
Create the environment variables needed by DDMD.
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
module load ddmd
```


Store the current environment in the pipeline.
```bash
jarvis pipeline env build +CONDA_OPENMM +CONDA_PYTORCH +DDMD_PATH
```


## 5.6. Add pkgs to the Pipeline
Add data_stagein to pipeline before ddmd.
- For `RUN_SCRIPT=vistsis` you need to stage in three different input directories:
```bash 
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$INPUT_PATH/vistdii,$INPUT_PATH/vistsis,$INPUT_PATH/visit_img,$PRETRAIN_MODEL_PATH \
mkdir_datapaths=$LOCAL_INPUT_PATH,$LOCAL_OUTPUT_PATH
```

- For other `RUN_SCRIPT`, you only need to stagein one directory:
```bash 
RUN_SCRIPT=pororo
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$INPUT_PATH/$RUN_SCRIPT \
mkdir_datapaths=$LOCAL_INPUT_PATH,$LOCAL_OUTPUT_PATH
```


Create a Jarvis pipeline with DDMD.
```bash
jarvis pipeline append ddmd runscript=$RUN_SCRIPT ddmd_path="`scspkg pkg src ddmd`/DDMD" local_exp_dir=$LOCAL_EXPERIMENT_PATH
```

## 5.7. Run the Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 5.8. Clean Data

To clean data produced by Hermes + DDMD:
```bash
jarvis pipeline clean
```



# 6. DDMD + Hermes on Node Local Storage
Every step the same as [DDMD + Hermes](#4-ddmd-with-hermes), except for when creating a Jarvis pipeline with Hermes, using the Hermes VFD interceptor:
- Example using `RUN_SCRIPT=vistsis` you need to stage in three different input directories.
```bash
# Setup env
RUN_SCRIPT=vistsis # can change to other datasets
EXPERIMENT_PATH=~/experiments/ddmd_run # NFS
INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
cd $EXPERIMENT_PATH; export PRETRAIN_MODEL_PATH=`realpath model_large.pth`

LOCAL_EXPERIMENT_PATH=/mnt/nvme/$USER/ddmd_run
LOCAL_INPUT_PATH=$LOCAL_EXPERIMENT_PATH/input_data
LOCAL_OUTPUT_PATH=$LOCAL_EXPERIMENT_PATH/output_data

# add pkg to pipeline
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$INPUT_PATH/vistdii,$INPUT_PATH/vistsis,$INPUT_PATH/visit_img,$PRETRAIN_MODEL_PATH \
mkdir_datapaths=$LOCAL_INPUT_PATH,$LOCAL_OUTPUT_PATH

jarvis pipeline append hermes_run --sleep=10 include=$LOCAL_EXPERIMENT_PATH

jarvis pipeline append hermes_api +vfd

jarvis pipeline append ddmd runscript=vistsis ddmd_path="`scspkg pkg src ddmd`/DDMD" update_envar=true local_exp_dir=$LOCAL_EXPERIMENT_PATH
```


# 7. DDMD + Hermes with Multinodes Slurm (TODO)
Multinodes DDMD is not supported yet.
```

### `builtin/builtin/dlio_benchmark/README.md`

```markdown
DLIO is an I/O benchmark for Deep Learning, aiming at emulating the I/O behavior of various deep learning applications.

# Installation

```bash
git clone https://github.com/argonne-lcf/dlio_benchmark
cd dlio_benchmark/
pip install .
```

# DLIO

## 1. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2. Create a Pipeline

The Jarvis pipeline will store all configuration data.
```bash
jarvis pipeline create dlio_test
```

## 4. Add pkgs to the Pipeline

Create a Jarvis pipeline
```bash
jarvis pipeline append dlio_benchmark workload=unet3d_a100 generate_data=True data_path=/path/to/generated_data checkpoint_path=/path/to/checkpoints
```
Note: you can modify the dlio_benchmark configuration file by changing the modifying the dlio_benchmark.yaml file directly, and then execute `jarvis ppl update` to update the configuration. 

## 5. Run Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 6. Clean Data

Clean produced data
```bash
jarvis pipeline clean
```
```

### `builtin/builtin/filebench/README.md`

```markdown
Filebench is a cloud workload generator.

# Installation

```bash
spack install filebench
```
```

### `builtin/builtin/fio/README.md`

```markdown
FIO

# Installation

```bash
spack install fio
```

# FIO
```

### `builtin/builtin/gadget2/README.md`

```markdown
GADGET is a freely available code for cosmological N-body/SPH simulations on massively parallel computers with distributed memory. GADGET uses an explicit communication model that is implemented with the standardized MPI communication interface. The code can be run on essentially all supercomputer systems presently in use, including clusters of workstations or individual PCs.

GADGET computes gravitational forces with a hierarchical tree algorithm (optionally in combination with a particle-mesh scheme for long-range gravitational forces) and represents fluids by means of smoothed particle hydrodynamics (SPH). The code can be used for studies of isolated systems, or for simulations that include the cosmological expansion of space, both with or without periodic boundary conditions. In all these types of simulations, GADGET follows the evolution of a self-gravitating collisionless N-body system, and allows gas dynamics to be optionally included. Both the force computation and the time stepping of GADGET are fully adaptive, with a dynamic range which is, in principle, unlimited.

https://wwwmpa.mpa-garching.mpg.de/gadget/

# Installation

```bash
spack install hdf5@1.14.1 gsl@2.1 fftw@2
scspkg create gadget2
cd $(scspkg pkg src gadget2)
git clone https://github.com/lukemartinlogan/gadget2.git
export GADGET2_PATH=$(scspkg pkg src gadget2)/gadget2
export FFTW_PATH=$(spack find --format "{PREFIX}" fftw@2)
```

# Create environment

```bash
spack load hdf5@1.14.1 gsl@2.1 fftw@2
jarvis env build gadget2 +GADGET2_PATH +FFTW_PATH
```

# Gassphere Pipeline

```bash
jarvis pipeline create gassphere
jarvis pipeline env copy gadget2
jarvis pipeline append gadget2
jarvis pkg configure gadget2 \
test_case=gadget2 \
out=${HOME}/gadget2
jarvis pipeline run
```

# NGenIC Pipeline

```bash
jarvis pipeline create gassphere
jarvis pipeline env copy gadget2
jarvis pipeline append gadget2
jarvis pkg configure gadget2 \
test_case=gassphere-ngen \
out=${HOME}/gadget2 \
ic=hello
jarvis pipeline run
```
```

### `builtin/builtin/gadget2_df/README.md`

```markdown
GADGET is a freely available code for cosmological N-body/SPH simulations on massively parallel computers with distributed memory. GADGET uses an explicit communication model that is implemented with the standardized MPI communication interface. The code can be run on essentially all supercomputer systems presently in use, including clusters of workstations or individual PCs.

GADGET computes gravitational forces with a hierarchical tree algorithm (optionally in combination with a particle-mesh scheme for long-range gravitational forces) and represents fluids by means of smoothed particle hydrodynamics (SPH). The code can be used for studies of isolated systems, or for simulations that include the cosmological expansion of space, both with or without periodic boundary conditions. In all these types of simulations, GADGET follows the evolution of a self-gravitating collisionless N-body system, and allows gas dynamics to be optionally included. Both the force computation and the time stepping of GADGET are fully adaptive, with a dynamic range which is, in principle, unlimited.

https://wwwmpa.mpa-garching.mpg.de/gadget/

# Installation

Check the README for gadget2.

# Create Pipeline

```bash
jarvis pipeline create ngenic
jarvis pipeline env copy gadget2
jarvis pipeline append gadget2_df
jarvis pkg configure gadget2_df \
nparticles=100000 \
nprocs=4
jarvis pipeline run
```
```

### `builtin/builtin/gray_scott/README.md`

```markdown
Gray-Scott is a 3D 7-Point stencil code

# Installation

```bash
scspkg create gray-scott
cd `scspkg pkg src gray-scott`
git clone https://github.com/pnorbert/adiosvm
cd adiosvm/Tutorial/gs-mpiio
mkdir build
pushd build
cmake ../ -DCMAKE_BUILD_TYPE=Release
make -j8
export GRAY_SCOTT_PATH=`pwd`
scspkg env set gray_scott GRAY_SCOTT_PATH="${GRAY_SCOTT_PATH}"
scspkg env prepend gray_scott PATH "${GRAY_SCOTT_PATH}"
module load gray_scott
spack load mpi adios2
```

# Gray Scott

## 1. Setup Environment

Create the environment variables needed by Gray Scott
```bash
module load gray_scott
spack load mpi
```````````

## 1. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Gray Scott.

```bash
jarvis pipeline create gray-scott-test
```

## 3. Save Environment

Store the current environment in the pipeline.
```bash
jarvis pipeline env build
```

## 4. Add pkgs to the Pipeline

Create a Jarvis pipeline with Gray Scott
```bash
jarvis pipeline append gray_scott
```

## 5. Run Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 6. Clean Data

Clean data produced by Gray Scott
```bash
jarvis pipeline clean
```

# Gray Scott With Hermes

## 1. Setup Environment

Create the environment variables needed by Hermes + Gray Scott
```bash
# On personal
spack install hermes@master adios2
spack load hermes adios2
# On Ares
module load hermes/master-feow7up adios2/2.9.0-mmkelnu
# export GRAY_SCOTT_PATH=${HOME}/adiosvm/Tutorial/gs-mpiio/build
export PATH="${GRAY_SCOTT_PATH}:$PATH"
```

## 2. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile.txt
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 3. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Hermes
and Gray Scott.

```bash
jarvis pipeline create gs-hermes
```

## 3. Save Environment

Store the current environment in the pipeline.
```bash
jarvis pipeline env build
```

## 4. Add pkgs to the Pipeline

Create a Jarvis pipeline with Hermes, the Hermes MPI-IO interceptor,
and gray-scott
```bash
jarvis pipeline append hermes --sleep=10 --output_dir=${HOME}/gray-scott
jarvis pipeline append hermes_api +mpi
jarvis pipeline append gray_scott
```

## 5. Run the Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 6. Clean Data

To clean data produced by Hermes + Gray-Scott:
```bash
jarvis pipeline clean
```
```

### `builtin/builtin/ior/README.md`

```markdown
LabStor is a distributed semi-microkernel for building data processing services.

# Installation

```bash
spack install ior mpi
```

# IOR

## 1. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2. Create a Pipeline

The Jarvis pipeline will store all configuration data.
```bash
jarvis pipeline create ior
```

## 3. Load Environment

Create the environment variables
```bash
spack load ior mpi
```````````

## 4. Add pkgs to the Pipeline

Create a Jarvis pipeline
```bash
jarvis pipeline append ior
```

## 5. Run Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 6. Clean Data

Clean produced data
```bash
jarvis pipeline clean
```
```

### `builtin/builtin/lammps/README.md`

```markdown
# LAMMPS

## what is lammps

LAMMPS is a classical molecular dynamics simulation code designed to
run efficiently on parallel computers.  It was developed at Sandia
National Laboratories, a US Department of Energy facility, with
funding from the DOE.  It is an open-source code, distributed freely
under the terms of the GNU Public License (GPL) version 2.


## what is the output of lammps
log file of thermodynamic info, text dump files of atom coordinates, velocities, other per-atom quantities, dump output on fixed and variable intervals, based timestep or simulated time, binary restart files, parallel I/O of dump and restart files, per-atom quantities (energy, stress, centro-symmetry parameter, CNA, etc.). user-defined system-wide (log file) or per-atom (dump file) calculations
custom partitioning (chunks) for binning, and static or dynamic grouping of atoms for analysis spatial, time, and per-chunk averaging of per-atom quantities time averaging and histogramming of system-wide quantities atom snapshots in native, XYZ, XTC, DCD, CFG, NetCDF, HDF5, ADIOS2, YAML formats on-the-fly compression of output and decompression of read in files.

## lammps tutorial
Please refer to this [website](https://docs.lammps.org/) for more details.
```

### `builtin/builtin/nyx_lya/README.md`

```markdown
Nyx is an adaptive mesh, massively-parallel, cosmological simulation code. 

# Installation

To compile the code we require C++11 compliant compilers that support MPI-2 or higher implementation. If threads or accelerators are used, we require OpenMP 4.5 or higher, Cuda 9 or higher, or HIP-Clang.

## 1. Install Dependencies


## 1. Install AMReX

```bash
git clone https://github.com/AMReX-Codes/amrex.git
pushd amrex
mkdir build
pushd build
cmake .. -DAMReX_HDF5=ON -DAMReX_PARTICLES=ON -DAMReX_PIC=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/path/to/amrex/install
make -j8
make install
popd
popd
```

## 2. Install Nyx

```bash
git clone https://github.com/AMReX-astro/Nyx.git
pushd Nyx
mkdir build
pushd build
cmake .. -DCMAKE_PREFIX_PATH=/path/to/amrex/install -DAMReX_DIR=/path/to/amrex/install/Tools/CMake/ -DNyx_SINGLE_PRECISION_PARTICLES=OFF -DNyx_OMP=OFF
make -j8
export NYX_PATH=`pwd`/Exec
popd
popd
```

# Nyx LyA

## 1. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Nyx LyA.

```bash
jarvis pipeline create nyx-lya-test
```

## 4. Add pkgs to the Pipeline

Create a Jarvis pipeline with Nyx LyA
```bash
jarvis pipeline append nyx_lya --nyx_install_path=$NYX_PATH --initial_z=190.0 --final_z=180.0 --plot_z_values="188.0 186.0" --output=/path/to/output_files
```
**nyx_install_path**: this argument is required, otherwise it will report an error.
You can use the default arguments for other arguments. But it may take a while.

## 5. Run Experiment

Run the experiment
```bash
jarvis pipeline run
```

## 6. Clean Data

Clean data produced by Nyx LyA
```bash
jarvis pipeline clean
```
```

### `builtin/builtin/orangefs/README.md`

```markdown
In this section we go over how to install and deploy OrangeFS.
NOTE: if running in Ares, OrangeFS is already installed, so skip
to section 5.3.

# Install Various Dependencies

```bash
sudo apt update
sudo apt install -y fuse
sudo apt install gcc flex bison libssl-dev libdb-dev linux-headers-$(uname -r) perl make libldap2-dev libattr1-dev
```

For fuse
```bash
sudo apt -y install fuse
spack install libfuse@2.9
```

NOTE: This package expects a working, passwordless SSH setup if you are using multiple nodes. On systems like Chameleon Cloud, you
must distribute the keys and set this up yourself before using jarvis. On single-node systems, SSH is not required.

# Install OrangeFS (Linux)

OrangeFS is located [on this website](http://www.orangefs.org/?gclid=CjwKCAjwgqejBhBAEiwAuWHioDo2uu8wel6WhiFqoBDgXMiVXc7nrykeE3sf3mIfDFVEt0_7SwRN8RoCdRYQAvD_BwE)
The official OrangeFS github is [here](https://github.com/waltligon/orangefs/releases/tag/v.2.9.8).

```bash
scspkg create orangefs
cd `scspkg pkg src orangefs`
wget https://github.com/waltligon/orangefs/releases/download/v.2.10.0/orangefs-2.10.0.tar.gz
tar -xvzf orangefs-2.10.0.tar.gz
cd orangefs
./prepare
./configure --prefix=`scspkg pkg root orangefs` --enable-shared --enable-fuse
make -j8
make install
scspkg env prepend orangefs ORANGEFS_PATH `scspkg pkg root orangefs`
```

# Using MPICH with OrangeFS

MPICH requires a special build when using OrangeFS. Apparantly it's for
performance, but it's a pain to have to go through the extra step.

```bash
scspkg create orangefs-mpich
cd `scspkg pkg src orangefs-mpich`
wget http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz --no-check-certificate
tar -xzf mpich-3.2.tar.gz
cd mpich-3.2
./configure --prefix=`scspkg pkg root orangefs-mpich` --enable-fast=O3 --enable-romio --enable-shared --with-pvfs2=`scspkg pkg root orangefs` --with-file-system=pvfs2
make -j8
make install
```

# Creating a pipeline

## Main Parmaeters
There are a few main parameters:
* ``ofs_data_dir``: The place where orangefs should store data or metadata. 
This needs to be a directory private to each node. For example, like /tmp or a burst buffer.
* ``mount``: Where the client should be mounted. This is where users will typically place data.
* ``ofs_mode``: The deployment method to use. Either fuse, kern, or ares.
* ``name``: The semantic name of the OrangeFS deployment. Typically just leave as default unless 
you have multiple deployments

## Performance Parameters
* ``stripe_size``: Size in bytes for stripes. Default 65536 (i.e., 64KB). 
* ``protocol``: Either tcp or ib. Only tcp has been tested.

## The Hostfile
OrangeFS can be picky about the hostfile. We recommend using only IP addresses
in your jarvis hostfile at this time when using OrangeFS.

An example hostfile for a single-node deployment is below:
```bash
echo '127.0.0.1' > ~/hostfile.txt
jarvis hostfile set ~/hostfile.txt
```

## libfuse
```bash
module load orangefs
jarvis pipeline create orangefs
jarvis pipeline env build +ORANGEFS_PATH
jarvis pipeline append orangefs \
mount=${HOME}/orangefs_client \
ofs_data_dir=${HOME}/ofs_data \
ofs_mode=fuse
```

## For kernel module
```bash
module load orangefs
jarvis pipeline create orangefs
jarvis pipeline env build +ORANGEFS_PATH
jarvis pipeline append orangefs \
mount=${HOME}/orangefs_client \
ofs_data_dir=/mnt/nvme/$USER/ofs_data \
ofs_mode=kern
```

## Ares Machine at IIT
```bash
module load orangefs
jarvis pipeline create orangefs
jarvis pipeline env build +ORANGEFS_PATH
jarvis pipeline append orangefs \
mount=${HOME}/orangefs_client \
ofs_data_dir=/mnt/nvme/$USER/ofs_data \
ofs_mode=ares
```
```

### `builtin/builtin/paraview/README.md`

```markdown
# paraview 
ParaView is an open-source data analysis and visualization application designed to handle large-scale scientific datasets. It supports interactive and batch processing for visualizing complex simulations and performing quantitative analysis.
```

### `builtin/builtin/pyflextrkr/README.md`

```markdown
The Python FLEXible object TRacKeR (PyFLEXTRKR) is a flexible atmospheric feature tracking software package.
See the [official repo](https://github.com/FlexTRKR/PyFLEXTRKR) for more detail.

# Table of Content
0. [Dependencies](#0-dependencies)
1. [Installation](#1-installation)
2. [Running Pyflextrkr](#2-running-pyflextrkr)
3. [Pyflextrkr with Slurm](#3-pyflextrkr-with-slurm)
4. [Pyflextrkr + Hermes](#4-pyflextrkr--hermes)
5. [Pyflextrkr on Node Local Storage](#5-pyflextrkr-on-node-local-storage)
6. [Pyflextrkr + Hermes on Node Local Storage](#6-pyflextrkr--hermes-on-node-local-storage)
7. [Pyflextrkr + Hermes with Multinodes Slurm (TODO)](#7-pyflextrkr--hermes-on-multinodes-slurm-todo)



# 0. Dependencies

## 0.1. conda
- Prepare Conda
Get the miniconda3 installation script and run it
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh.sh
```

## 0.2. jarvis-cd & scspkg
Follow steps here: https://github.com/grc-iit/jarvis-cd


## 0.3. spack
Spack is used to install HDF5, MPICH, and Hermes.
Install spack steps are here: https://spack.readthedocs.io/en/latest/getting_started.html#installation

## 0.4. HDF5 (1.14.0+)
HDF5 is require, (1.14.0+) is required by Hermes and h5py==3.8.0.

Use spack to install hdf5
```bash
spack install hdf5@1.14.0+hl~mpi
```

## 0.5. MPI
Either OpenMPI or MPICH works, this is required by Hermes and mpi4py


Use spack to install mpich
```bash
spack install mpich@3.4.3
```

## 0.6. Installation Tools
You need `wget` to download the datasets online:
- wget
You can install wget either with `apt-get` or `spack`
```bash
sudo apt-get install wget
# or
spack install wget
spack load wget
# check if wget is usable
which wget
```



# 1. Installation

## 1.1 create pyflextrkr scs package
```bash
scspkg create pyflextrkr
cd `scspkg pkg src pyflextrkr`
git clone https://github.com/candiceT233/PyFLEXTRKR
cd PyFLEXTRKR
git switch ares # User the ares branch
scspkg env set pyflextrkr PYFLEXTRKR_PATH="`pwd`"
```


## 1.2 Prepare conda environment and python packages:
```bash
cd `scspkg pkg src pyflextrkr`/PyFLEXTRKR

YOUR_HDF5_DIR="`which h5cc |sed 's/.\{9\}$//'`"

conda env create -f ares_flextrkr.yml -n flextrkr
conda activate flextrkr
pip install -e .
HDF5_MPI="OFF" HDF5_DIR=${YOUR_HDF5_DIR} pip install --no-cache-dir --no-binary=h5py h5py==3.8.0
pip install xarray[io] mpi4py
conda deactivate
```



# 2. Running Pyflextrkr
Example is using `TEST_NAME=run_mcs_tbpfradar3d_wrf` (only supported with dataset download).
## 2.1. Setup Environment
Currently setup input path in a shared storage, below is a example on Ares cluster.
```bash
TEST_NAME=run_mcs_tbpfradar3d_wrf
EXPERIMENT_PATH=~/experiments/pyflex_run # NFS

export EXPERIMENT_INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
scspkg env set pyflextrkr EXPERIMENT_INPUT_PATH=$EXPERIMENT_INPUT_PATH
mkdir -p $EXPERIMENT_INPUT_PATH
```

## 2.2. Download Input Data
Setup example input data `wrf_tbradar.tar.gz` and path.to `run_mcs_tbpfradar3d_wrf.tar.gz`
```bash
cd $EXPERIMENT_INPUT_PATH
wget https://portal.nersc.gov/project/m1867/PyFLEXTRKR/sample_data/tb_radar/wrf_tbradar.tar.gz -O $TEST_NAME.tar.gz
mkdir $TEST_NAME
tar -xvzf $TEST_NAME.tar.gz -C $TEST_NAME

# Remove downloaded tar file
rm -rf $EXPERIMENT_INPUT_PATH/$TEST_NAME.tar.gz
```


## 2.3. Create a Resource Graph

If you haven't already, create a resource graph. This only needs to be done
once throughout the lifetime of Jarvis. No need to repeat if you have already
done this for a different pipeline.

For details building resource graph, please refer to https://github.com/grc-iit/jarvis-cd/wiki/2.-Resource-Graph.

If you are running distributed tests, set path to the hostfile you are  using.
```bash
jarvis hostfile set /path/to/hostfile
```

Next, collect the resources from each of those pkgs. Walkthrough will give
a command line tutorial on how to build the hostfile.
```bash
jarvis resource-graph build +walkthrough
```

## 2.4 Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Pyflextrkr.

```bash
jarvis pipeline create pyflextrkr_test
```

## 2.5. Save Environment
Create the environment variables needed by Pyflextrkr.
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
module load pyflextrkr
```
<!-- conda activate flextrkr -->

Store the current environment in the pipeline.
```bash
jarvis env build pyflextr +PYFLEXTRKR_PATH +EXPERIMENT_INPUT_PATH
jarvis pipeline env copy pyflextr
```

## 2.6. Add pkgs to the Pipeline
** Currently only support running `runscript=run_mcs_tbpfradar3d_wrf` **

Create a Jarvis pipeline with Pyflextrkr.
```bash
jarvis pipeline append pyflextrkr runscript=run_mcs_tbpfradar3d_wrf
```


## 2.7. Run Experiment

Run the experiment, output are generated in `$EXPERIMENT_INPUT_PATH/output_data`.
```bash
jarvis pipeline run
```

## 2.8. Clean Data

Clean data produced by Pyflextrkr
```bash
jarvis pipeline clean
```



# 3. Pyflextrkr With Slurm

## 3.1 Local Cluster
Do the above and `ppn` must match `nprocesses`
```bash
jarvis pipeline sbatch job_name=pyflex_test nnodes=1 ppn=8 output_file=./pyflex_test.out error_file=./pyflex_test.err
```

## 3.2 Multi Nodes Cluster
Do the above and `ppn` must greater than match `nprocesses`/`nnodes` 
    (e.g. `nnodes=2 ppn=8` allocates 16 processes in total, and `nprocesses` must not greater than 16)

Configure Pyflextrkr to parallel run mode with MPI-Dask (0: serial, 1: Dask one-node cluster, 2: Dask multinode cluster)
```bash
jarvis pkg configure pyflextrkr run_parallel=2 nprocesses=8
```

```bash
jarvis pipeline sbatch job_name=pyflex_2ntest nnodes=2 ppn=4 output_file=./pyflex_2ntest.out error_file=./pyflex_2ntest.err
```



# 4. Pyflextrkr + Hermes

## 4.0. Dependencies
### 4.0.1 HDF5
Hermes must compile with HDF5, makesure [download HDF5-1.14.0 with spack](#4-hdf5-1140).

### 4.0.2 Install Hermes dependencies with spack
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
spack install hermes_shm ^hdf5@1.14.0+hl~mpi ^mpich@3.4.3
```

### 4.0.3 Install Hermes with scspkg
```bash
spack load hermes_shm
scspkg create hermes
cd `scspkg pkg src hermes`
git clone https://github.com/HDFGroup/hermes
cd hermes
mkdir build
cd build
cmake ../ -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX=`scspkg pkg root hermes` \
    -DHERMES_ENABLE_MPIIO_ADAPTER="ON" \
    -DHERMES_MPICH="ON" \
    -DHERMES_ENABLE_POSIX_ADAPTER="ON" \
    -DHERMES_ENABLE_STDIO_ADAPTER="ON" \
    -DHERMES_ENABLE_VFD="ON" \

```

## 4.1. Setup Environment

Create the environment variables needed by Hermes + Pyflextrkr
```bash
spack load hermes_shm
module load hermes pyflextrkr
```

## 4.2. Create a Resource Graph

Same as [above](#2-create-a-resource-graph).

## 4.3. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Hermes
and Pyflextrkr.

```bash
jarvis pipeline create hermes_pyflextrkr_test
```

## 4.4. Save Environment

Store the current environment in the pipeline.
```bash
jarvis pipeline env build +PYFLEXTRKR_PATH
```

## 4.5. Add pkgs to the Pipeline

Create a Jarvis pipeline with Hermes, the Hermes VFD interceptor,
and pyflextrkr (must use `flush_mode=sync` to prevent [this error](#oserror-log))
```bash
jarvis pipeline append hermes_run --sleep=10 include=$EXPERIMENT_PATH flush_mode=sync
jarvis pipeline append hermes_api +vfd
jarvis pipeline append pyflextrkr runscript=$TEST_NAME update_envar=true
```

## 4.6. Run the Experiment

Run the experiment, output are generated in `$EXPERIMENT_INPUT_PATH/output_data`.
```bash
jarvis pipeline run
```

## 4.7. Clean Data

To clean data produced by Hermes + Pyflextrkr:
```bash
jarvis pipeline clean
```



# 5. Pyflextrkr on Node Local Storage
For cluster that has node local storage, you can stagein data from shared storage, then run pyflextrkr.

## 5.1 Setup Environment
Currently setup DEFAULT input path in a shared storage, below is a example on Ares cluster using node local nvme.


The shared storage path is same as before:
```bash
export TEST_NAME=run_mcs_tbpfradar3d_wrf
EXPERIMENT_PATH=~/experiments/pyflex_run # NFS
EXPERIMENT_INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
mkdir -p $EXPERIMENT_INPUT_PATH
```
Setup the node local experiment paths:
```bash
LOCAL_EXPERIMENT_PATH=/mnt/nvme/$USER/pyflex_run
LOCAL_INPUT_PATH=$LOCAL_EXPERIMENT_PATH/input_data
```

## 5.2. Download Input Data
Same as [above](#22-download-input-data).

## 5.3. Create a Resource Graph
Same as [above](#23-create-a-resource-graph)

## 5.4. Create a Pipeline

The Jarvis pipeline will store all configuration data needed by Pyflextrkr.

```bash
jarvis pipeline create pyflextrkr_local
```

## 5.5. Save Environment
Create the environment variables needed by Pyflextrkr.
```bash
spack load hdf5@1.14.0+hl~mpi mpich@3.4.3
module load pyflextrkr
```


Store the current environment in the pipeline.
```bash
jarvis pipeline env build +PYFLEXTRKR_PATH
```

## 5.6. Add pkgs to the Pipeline
Add data_stagein to pipeline before pyflextrkr.
```bash 
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$EXPERIMENT_INPUT_PATH/$TEST_NAME \
mkdir_datapaths=$LOCAL_INPUT_PATH
```

Create a Jarvis pipeline with Pyflextrkr.
```bash
jarvis pipeline append pyflextrkr runscript=$TEST_NAME local_exp_dir=$LOCAL_INPUT_PATH
```

## 5.7. Run the Experiment

Run the experiment, output are generated in `$LOCAL_INPUT_PATH/output_data`.
```bash
jarvis pipeline run
```

## 5.8. Clean Data

To clean data produced by Hermes + Pyflextrkr:
```bash
jarvis pipeline clean
```



# 6. Pyflextrkr + Hermes on Node Local Storage
Every step the same as [Pyflextrkr + Hermes](#4-pyflextrkr--hermes), except for when creating a Jarvis pipeline with Hermes, using the Hermes VFD interceptor:
```bash
# Setup env
TEST_NAME=run_mcs_tbpfradar3d_wrf
EXPERIMENT_PATH=~/experiments/pyflex_run # NFS
INPUT_PATH=$EXPERIMENT_PATH/input_data # NFS
mkdir -p $EXPERIMENT_INPUT_PATH

LOCAL_EXPERIMENT_PATH=/mnt/nvme/$USER/pyflex_run
LOCAL_INPUT_PATH=$LOCAL_EXPERIMENT_PATH/input_data

# add pkg to pipeline
jarvis pipeline append data_stagein dest_data_path=$LOCAL_INPUT_PATH \
user_data_paths=$EXPERIMENT_INPUT_PATH/$TEST_NAME \
mkdir_datapaths=$LOCAL_INPUT_PATH

jarvis pipeline append hermes_run --sleep=10 include=$LOCAL_EXPERIMENT_PATH

jarvis pipeline append hermes_api +vfd

jarvis pipeline append pyflextrkr runscript=$TEST_NAME update_envar=true local_exp_dir=$LOCAL_INPUT_PATH
```



# 7. Pyflextrkr + Hermes on Multinodes Slurm (TODO)
Steps are the same as [Pyflextrkr with Slurm](#3-pyflextrkr-With-slurm), but not working yet due to OSError.

## OSError Log
```log
2024-01-03 18:49:03,523 - pyflextrkr.idfeature_driver - INFO - Identifying features from raw data
2024-01-03 18:49:04,969 - pyflextrkr.idfeature_driver - INFO - Total number of files to process: 17
free(): invalid size
2024-01-03 18:49:07,944 - distributed.worker - WARNING - Compute Failed
Key:       idclouds_tbpf-0bb7839d-ac6e-4e51-b309-ec2bc6667641
Function:  execute_task
args:      ((<function idclouds_tbpf at 0x7fce75d6da80>, '/home/mtang11/experiments/pyflex_runs/input_data/run_mcs_tbpfradar3d_wrf/wrfout_rainrate_tb_zh_mh_2015-05-06_04:00:00.nc', (<class 'dict'>, [['ReflThresh_lowlevel_gap', 20.0], ['abs_ConvThres_aml', 45.0], ['absolutetb_threshs', [160, 330]], ['area_thresh', 36], ['background_Box', 12.0], ['clouddata_path', '/home/mtang11/experiments/pyflex_runs/input_data/run_mcs_tbpfradar3d_wrf/'], ['clouddatasource', 'model'], ['cloudidmethod', 'label_grow'], ['cloudtb_cloud', 261.0], ['cloudtb_cold', 241.0], ['cloudtb_core', 225.0], ['cloudtb_warm', 261.0], ['col_peakedness_frac', 0.3], ['dask_tmp_dir', '/tmp/pyflextrkr_test'], ['databasename', 'wrfout_rainrate_tb_zh_mh_'], ['datatimeresolution', 1.0], ['dbz_lowlevel_asl', 2.0], ['dbz_thresh', 10], ['duration_range', [2, 300]], ['echotop_gap', 1], ['enddate', '20150506.1600'], ['etop25dBZ_Thresh', 10.0], ['feature_type', 'tb_pf_radar3d'], ['feature_varname', 'feature_number'], ['featuresize_varname',
kwargs:    {}
Exception: "OSError('Unable to synchronously open file (file signature not found)')"

Traceback (most recent call last):
  File "/mnt/common/mtang11/scripts/scspkg/packages/pyflextrkr/src/PyFLEXTRKR/runscripts/run_mcs_tbpfradar3d_wrf.py", line 115, in <module>
    idfeature_driver(config)
  File "/mnt/common/mtang11/scripts/scspkg/packages/pyflextrkr/src/PyFLEXTRKR/pyflextrkr/idfeature_driver.py", line 66, in idfeature_driver
    final_result = dask.compute(*results)
                   ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/dask/base.py", line 595, in compute
    results = schedule(dsk, keys, **kwargs)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/distributed/client.py", line 3243, in get
    results = self.gather(packed, asynchronous=asynchronous, direct=direct)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/distributed/client.py", line 2368, in gather
    return self.sync(
           ^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/distributed/utils.py", line 351, in sync
    return sync(
           ^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/distributed/utils.py", line 418, in sync
    raise exc.with_traceback(tb)
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/distributed/utils.py", line 391, in f
    result = yield future
             ^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/tornado/gen.py", line 767, in run
    value = future.result()
            ^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/distributed/client.py", line 2231, in _gather
    raise exception.with_traceback(traceback)
  File "/mnt/common/mtang11/scripts/scspkg/packages/pyflextrkr/src/PyFLEXTRKR/pyflextrkr/idclouds_tbpf.py", line 98, in idclouds_tbpf
    rawdata = xr.open_dataset(filename, engine='h5netcdf') # , engine='h5netcdf' netcdf4 h5netcdf
      ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/api.py", line 566, in open_dataset
    backend_ds = backend.open_dataset(
      ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/h5netcdf_.py", line 413, in open_dataset
    store = H5NetCDFStore.open(
  ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/h5netcdf_.py", line 176, in open
    return cls(manager, group=group, mode=mode, lock=lock, autoclose=autoclose)
  ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/h5netcdf_.py", line 127, in __init__
    self._filename = find_root_and_group(self.ds)[0].filename
  ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/h5netcdf_.py", line 187, in ds
    return self._acquire()
  ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/h5netcdf_.py", line 179, in _acquire
    with self._manager.acquire_context(needs_lock) as root:
  ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/file_manager.py", line 198, in acquire_context
    file, cached = self._acquire_with_cache_info(needs_lock)
  ^^^^^^^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/xarray/backends/file_manager.py", line 216, in _acquire_with_cache_info
    file = self._opener(*self._args, **kwargs)
^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/h5netcdf/core.py", line 1051, in __init__
    self._h5file = self._h5py.File(
^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/h5py/_hl/files.py", line 567, in __init__
    fid = make_fid(name, mode, userblock_size, fapl, fcpl, swmr=swmr)
^^^^^^^^^^^
  File "/home/mtang11/miniconda3/envs/flextrkr/lib/python3.11/site-packages/h5py/_hl/files.py", line 231, in make_fid
    fid = h5f.open(name, flags, fapl=fapl)
  ^^^^^^^^^^^^^^^^^
  File "h5py/_objects.pyx", line 54, in h5py._objects.with_phil.wrapper
  File "h5py/_objects.pyx", line 55, in h5py._objects.with_phil.wrapper
  File "h5py/h5f.pyx", line 106, in h5py.h5f.open
OSError: Unable to synchronously open file (file signature not found)
```
```

### `builtin/builtin/pymonitor/README.md`

```markdown

```

### `builtin/builtin/redis-benchmark/README.md`

```markdown
LabStor is a distributed semi-microkernel for building data processing services.

# Installation

```bash
spack install redis
```
```

### `builtin/builtin/redis/README.md`

```markdown
Redis is a key-value store

# Installation

```bash
spack install redis
```
```

### `builtin/builtin/spark_cluster/README.md`

```markdown
# Installation

Manual build:
```
spack install openjdk@11
spack load openjdk@11
scspkg create spark
cd `scspkg pkg src spark`
wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1.tgz
tar -xzf spark-3.5.1.tgz
cd spark-3.5.1
./build/mvn -T 16 -DskipTests clean package
scspkg env set spark SPARK_SCRIPTS=${PWD}
scspkg env prepend spark PATH "${PWD}/bin"
module load spark
```
NOTE: this took 30min in Ares.

With spack (doesn't seem to work, sorry):
```
spack install spark
spack load spark
scspkg create spark-env
scspkg env set spark-env SPARK_SCRIPTS=`spack find --format "{PREFIX}" spark`
module load spark-env
```

Additional configuration documentation 
[here](https://spark.apache.org/docs/latest/spark-standalone.html).

# Create the Jarvis pipeline

```
jarvis pipeline create spark
```

# Build the Jarvis environment

```
jarvis pipeline env build +SPARK_SCRIPTS
```

# Append the Spark Cluster Pkg

```
jarvis pipeline append spark_cluster
```

# Run the pipeline

```
jarvis pipeline run
```
```

### `builtin/builtin/wrf/README.md`

```markdown
# WRF 

## what is the WRF application?
WRF is a state-of-the-art atmospheric modeling system designed for both meteorological research and numerical weather prediction. It offers a host of options for atmospheric processes and can run on a variety of computing platforms. WRF excels in a broad range of applications across scales ranging from tens of meters to thousands of kilometers, including the following.

– Meteorological studies
– Real-time NWP
– Idealized simulations
– Data assimilation
– Earth system model coupling
– Model training and educational support

Here is the workflow for the WRF.
![WRF_workflow](wrf_workflow.png)
As shown in the diagram, the WRF Modeling System consists of the following programs.

### WRF Preprocessing System (WPS) (WPS)

### Initialization (Real and Ideal)

### WRF-ARW Solver (WRF)

### WRF Data Assimilation (WRFDA) (WRFDA)

### Post-processing, Analysis, and Visualization Tools

### WRF Preprocessing System (WPS)
The WPS is used for real-data simulations. Its functions are to 1) define simulation domains; 2) interpolate terrestrial data (e.g., terrain, landuse, and soil types) to the simulation domain; and 3) degrib and interpolate meteorological input data from an outside model to the simulation domain.

### Initialization
The WRF model is capable of simulating both real- and ideal-data cases. ideal.exe is a program that simulates in a controlled environment. Idealized simulations are initiated from an included initial condition file from an existing sounding, and assumes a simplified orography. Real-data cases use output from the WPS, which includes meteorological input originally generated from a previously-run external analysis or forecast model (e.g., GFS) as input to the real.exe program.





### WRF Data Assimilation (WRFDA)
WRF Data Assimilation (WRFDA) is an optional program used to ingest observations into interpolated analysis created by WPS. It may also be used to update the WRF model’s initial conditions by running in “cycling” mode. WRFDA’s primary features are:

The capability of 3D and 4D hybrid data assimilation (Variational + Ensemble)

Based on an incremental variational data assimilation technique

Tangent linear and adjoint of WRF are fully integrated with WRF for 4D-Var

Utilizes the conjugate gradient method to minimize cost function in the analysis control variable space

Analysis on an un-staggered Arakawa A-grid

Analysis increments interpolated to staggered Arakawa C-grid, which is then added to the background (first guess) to get the final analysis of the WRF-model grid

Conventional observation data input may be supplied in either ASCII format via the obsproc utility, or PREPBUFR format

Multiple-satellite observation data input may be supplied in BUFR format

Two fast radiative transfer models, CRTM and RTTOV, are interfaced to WRFDA to serve as satellite radiance observation operator

Variational bias correction for satellite radiance data assimilation

All-sky radiance data assimilation capability

Multiple radar data (reflectivity & radial velocity) input is supplied through ASCII format

Multiple outer loop to address nonlinearity




### Post-processing, Analysis, and Visualization Tools
Several post-processing programs are supported, including RIP (based on NCAR Graphics), NCAR Graphics Command Language (NCL), and conversion programs for other readily-available graphics packages (e.g., GrADS).

### wrf-python (wrf-python) 
is a collection of diagnostic and interpolation routines for use with output from the WRF model.

### NCL (NCAR Command Language) 
is a free, interpreted language designed specifically for scientific data processing and visualization. NCL has robust file input and output. It can read in netCDF, HDF4, HDF4-EOS, GRIB, binary and ASCII data. The graphics are world-class and highly customizable.

### RIP (Read/Interpolate/Plot) 
is a Fortran program that invokes NCAR Graphics routines for the purpose of visualizing output from gridded meteorological data sets, primarily from mesoscale numerical models.

### ARWpost 
is a package that reads-in WRF-ARW model data and creates GrADS output files.


## what this application generate:
For researchers, WRF can produce simulations based on actual atmospheric conditions (i.e., from observations and analyses) or idealized conditions. WRF offers operational forecasting a flexible and computationally-efficient platform, while reflecting recent advances in physics, numerics, and data assimilation contributed by developers from the expansive research community. WRF is currently in operational use at NCEP and other national meteorological centers as well as in real-time forecasting configurations at laboratories, universities, and companies. WRF has a large worldwide community of registered users, and NCAR provides regular workshops and tutorials on it.


###  Key Input Parameters (WRF)

# WRF Namelist Configuration: &time_control

This document provides a detailed overview of the parameters found in the `&time_control` section of the WRF `namelist.input` file. These settings govern the simulation timing, duration, input/output (I/O) operations, and restart capabilities.

---

##  Simulation Time & Duration

These parameters define the total length and the specific start/end dates of the simulation.

| Namelist Parameter | Default Setting | Description | Domain Scope |
| :--- | :--- | :--- | :--- |
| **`run_days`** | `0` | Simulation length in days. | Single Entry |
| **`run_hours`** | `0` | Simulation length in hours. | Single Entry |
| **`run_minutes`** | `0` | Simulation length in minutes. | Single Entry |
| **`run_seconds`** | `0` | Simulation length in seconds. Use any combination of `run_*` for the full duration. | Single Entry |
| **`start_year`** | `2019` | 4-digit year for the simulation start time. | Per Domain (`max_dom`) |
| **`start_month`** | `09` | 2-digit month for the simulation start time. | Per Domain (`max_dom`) |
| **`start_day`** | `04` | 2-digit day for the simulation start time. | Per Domain (`max_dom`) |
| **`start_hour`** | `12` | 2-digit hour for the simulation start time. | Per Domain (`max_dom`) |
| **`start_minute`** | `0` | 2-digit minute for the simulation start time. | Per Domain (`max_dom`) |
| **`start_second`** | `0` | 2-digit second for the simulation start time. | Per Domain (`max_dom`) |
| **`end_year`** | `2019` | 4-digit year for the simulation end time. | Per Domain (`max_dom`) |
| **`end_month`** | `09` | 2-digit month for the simulation end time. | Per Domain (`max_dom`) |
| **`end_day`** | `06` | 2-digit day for the simulation end time. | Per Domain (`max_dom`) |
| **`end_hour`** | `00` | 2-digit hour for the simulation end time. | Per Domain (`max_dom`) |
| **`end_minute`** | `0` | 2-digit minute for the simulation end time. | Per Domain (`max_dom`) |
| **`end_second`** | `0` | 2-digit second for the simulation end time. | Per Domain (`max_dom`) |
| **`interval_seconds`**| `10800` | Time interval (seconds) between lateral boundary condition files from WPS. | Single Entry |

> **Note:** `run_*` parameters take precedence in `wrf.exe`, while `real.exe` uses `start_*` and `end_*` times.

---

##  File I/O and History

Controls for writing history output files (e.g., `wrfout_d<domain>_<date>`).

| Namelist Parameter | Default Setting | Description | Domain Scope |
| :--- | :--- | :--- | :--- |
| **`history_interval`** | `60` | Frequency (minutes) for writing to history files. `_d/h/m/s` can be used. | Per Domain (`max_dom`) |
| **`history_begin`** | `0` | Time (minutes) from run start to begin writing history files. `_d/h/m/s` can be used. | Per Domain (`max_dom`) |
| **`frames_per_outfile`** | `1` | Number of history output times to bundle into a single output file. | Per Domain (`max_dom`) |
| **`output_ready_flag`** | `.true.` | Writes an empty `wrfoutReady_d<domain>` file for post-processing scripts to check completion. | Single Entry |
| **`io_form_history`** | `2` | I/O format for history files. Common options include: <br> • **2**: netCDF <br> • **11**: Parallel netCDF <br> • **102**: Split netCDF files (one per processor) | Single Entry |

---

##  Restart Controls

Parameters to manage simulation restarts from a previous state.

| Namelist Parameter | Default Setting | Description | Domain Scope |
| :--- | :--- | :--- | :--- |
| **`restart`** | `.false.` | Set to `.true.` if this is a restart simulation. | Single Entry |
| **`restart_interval`** | `1440` | Interval (minutes) for writing restart files (`wrfrst_*`). | Single Entry |
| **`override_restart_intervals`** | `.false.` | If `.true.`, uses this namelist's `restart_interval` instead of the one in the `wrfrst` file. | Single Entry |
| **`write_hist_at_0h_rst`** | `.false.` | If `.true.`, a history file will be written at the initial time of a restart run. | Single Entry |
| **`reset_simulation_start`** | `.false.` | If `.true.`, overwrites the simulation start date with the forecast start time from the restart file. | Single Entry |
| **`io_form_restart`**| `2` | I/O format for restart files. Options are similar to `io_form_history`. | Single Entry |

---

##  Input/Output Naming and Formatting

Define the names and formats of auxiliary input and output files.

| Namelist Parameter | Default Setting | Description | Domain Scope |
| :--- | :--- | :--- | :--- |
| **`input_from_file`** | `.true.` | Whether to use input files for nested domains. | Per Domain (`max_dom`) |
| **`fine_input_stream`** | `0` | Selects fields for nest initialization. <br> • **0**: All fields are used. <br> • **2**: Only fields from input stream 2 are used. | Per Domain (`max_dom`) |
| **`auxinput1_inname`**| `met_em.d<domain>.<date>` | Name of the input file from WPS. | Single Entry |
| **`auxinput4_inname`**| `wrflowinp_d<domain>` | Name of the input file for the lower boundary (e.g., SST). | Single Entry |
| **`auxinput4_interval`**| `360` | Interval (minutes) for the lower boundary file when `sst_update=1`. | Per Domain (`max_dom`) |
| **`io_form_input`** | `2` | I/O format of the input (`met_em`) files. | Single Entry |
| **`io_form_boundary`**| `2` | I/O format of the boundary (`wrfbdy`) files. | Single Entry |
| **`io_form_auxinput2`**| `2` | I/O format for auxiliary input stream 2. | Single Entry |
| **`auxhist9_outname`**| `auxhist9_d<domain>_<date>` | File name for auxiliary history output stream 9. | Single Entry |
| **`auxhist9_interval`**| `10` | Interval (minutes) for auxiliary history output stream 9. | Per Domain (`max_dom`) |
| **`nocolons`** | `.false.` | If `.true.`, replaces colons (`:`) with underscores (`_`) in output filenames. | Single Entry |

---

##  Diagnostics and Debugging

Options for enabling diagnostic print-outs and debugging information.

| Namelist Parameter | Default Setting | Description | Domain Scope |
| :--- | :--- | :--- | :--- |
| **`diag_print`** | `0` | Prints time series model diagnostics. <br> • **0**: No print. <br> • **1**: Prints domain-averaged pressure tendencies. <br> • **2**: Option 1 plus rainfall and heat fluxes. | Single Entry |
| **`debug_level`** | `0` | Increases debugging print-outs. Higher values (e.g., `50`, `200`) produce more verbose output. | Single Entry |
| **`output_diagnostics`**| `0` | Set to `1` to add 48 surface diagnostic arrays (max/min/mean/std) to the output. | Single Entry |
| **`nwp_diagnostics`** | `0` | Set to `1` to add several NWP diagnostic fields to the output file. | Single Entry |
```

### `builtin/builtin/ycsbc/README.md`

```markdown
Redis is a key-value store

# Installation

```bash
spack install redis
```
```

### `docs/README.md`

```markdown
# Jarvis CD Utility Classes Documentation

This documentation describes the utility classes implemented for the Jarvis CD project. These classes provide essential functionality for command-line argument parsing and host management in distributed computing environments.

## Overview

The `jarvis_cd.util` package contains two main utility classes:

1. **ArgParse** - Custom command-line argument parser with advanced features
2. **Hostfile** - Host management with pattern expansion and IP resolution

Both classes are designed to work together to provide a comprehensive foundation for building command-line tools and distributed computing applications.

## Quick Start

### Basic Imports

```python
from jarvis_cd.util.argparse import ArgParse
from jarvis_cd.util.hostfile import Hostfile
```

### Simple Example

```python
# Create a hostfile
hostfile = Hostfile(text="node-[01-05]", find_ips=False)
print(f"Hosts: {hostfile.host_str()}")  # node-01,node-02,node-03,node-04,node-05

# Create an argument parser
class MyParser(ArgParse):
    def define_options(self):
        self.add_menu('')
        self.add_cmd('run')
        self.add_args([
            {'name': 'nodes', 'type': int, 'required': True, 'pos': True}
        ])
    
    def run(self):
        print(f"Running with {self.kwargs['nodes']} nodes")

parser = MyParser()
parser.define_options()
parser.parse(['run', '4'])  # Running with 4 nodes
```

## Class Documentation

### [ArgParse Class](./argparse.md)

A sophisticated command-line argument parser supporting:
- **Menu/Command Structure**: Hierarchical organization of commands
- **Argument Types**: Positional, keyword, list, and remainder arguments  
- **Advanced Features**: Command aliases, argument ranking, type casting
- **Custom Handlers**: Automatic method dispatch for commands

**Key Features**:
- Complex argument structures with classes and ranking
- List arguments with set and append modes
- Automatic type conversion (str, int, bool, list)
- Command aliases and flexible syntax
- Comprehensive error handling

**Use Cases**:
- Building CLI applications with subcommands
- Scientific computing parameter management
- Distributed computing job configuration
- Complex workflow orchestration

### [Hostfile Class](./hostfile.md)

A powerful host management system supporting:
- **Pattern Expansion**: Bracket notation for host ranges (`node-[01-10]`)
- **Multiple Sources**: Files, text, manual lists
- **IP Resolution**: Automatic hostname-to-IP mapping
- **Host Operations**: Subset, copy, enumerate, string formatting

**Key Features**:
- Numeric and alphabetic range expansion
- Zero-padding preservation in numeric ranges
- Multi-line hostfile support
- Local vs. distributed detection
- Performance optimizations for large host sets

**Use Cases**:
- Cluster job submission
- Distributed computing node management
- Network administration tools
- Load balancing configuration

## Integration Patterns

### CLI Application with Host Management

```python
class ClusterApp(ArgParse):
    def define_options(self):
        self.add_menu('')
        self.add_cmd('deploy', aliases=['d'])
        self.add_args([
            {
                'name': 'hostfile',
                'msg': 'Path to hostfile',
                'type': str,
                'required': True,
                'pos': True
            },
            {
                'name': 'app_path',
                'msg': 'Application to deploy',
                'type': str,
                'required': True,
                'pos': True
            },
            {
                'name': 'nodes',
                'msg': 'Number of nodes to use',
                'type': int,
                'default': None
            },
            {
                'name': 'dry_run',
                'msg': 'Perform dry run',
                'type': bool,
                'default': False
            }
        ])
    
    def deploy(self):
        # Load hostfile
        hostfile = Hostfile(path=self.kwargs['hostfile'])
        
        # Use subset if specified
        if self.kwargs['nodes']:
            hostfile = hostfile.subset(self.kwargs['nodes'])
        
        if self.kwargs['dry_run']:
            print(f"Would deploy {self.kwargs['app_path']} to:")
            for hostname in hostfile:
                print(f"  - {hostname}")
        else:
            print(f"Deploying to {len(hostfile)} hosts...")
            self._deploy_to_hosts(hostfile, self.kwargs['app_path'])

# Usage: python app.py deploy /etc/hostfile.txt /path/to/app --nodes=5 --dry_run=true
```

### Batch Job Processor

```python
class BatchProcessor(ArgParse):
    def define_options(self):
        self.add_menu('batch', msg="Batch processing commands")
        
        self.add_cmd('batch submit')
        self.add_args([
            {
                'name': 'job_script',
                'type': str,
                'required': True,
                'pos': True,
                'class': 'files',
                'rank': 0
            },
            {
                'name': 'nodes',
                'msg': 'Node specifications',
                'type': list,
                'aliases': ['n'],
                'args': [
                    {'name': 'pattern', 'type': str},
                    {'name': 'count', 'type': int}
                ]
            }
        ])
    
    def batch_submit(self):
        # Process node specifications
        all_hosts = []
        for node_spec in self.kwargs.get('nodes', []):
            pattern = node_spec['pattern']
            count = node_spec['count']
            
            hostfile = Hostfile(text=pattern, find_ips=False)
            subset = hostfile.subset(count)
            all_hosts.extend(subset.hosts)
        
        print(f"Submitting job to hosts: {','.join(all_hosts)}")
        self._submit_job(self.kwargs['job_script'], all_hosts)

# Usage: python batch.py batch submit job.sh --n "(node-[01-10], 3)" --n "(gpu-[a-d], 2)"
```

## Testing

Both classes include comprehensive test suites:

- **ArgParse Tests**: `test/unit/test_argparse.py` (13 test cases)
- **Hostfile Tests**: `test/unit/test_hostfile.py` (30 test cases)

Run tests with:
```bash
python -m pytest test/unit/ -v
```

## Architecture Notes

### Design Principles

1. **Flexibility**: Support multiple input/output formats and use cases
2. **Performance**: Efficient parsing and processing for large datasets
3. **Extensibility**: Easy to subclass and extend for specific needs
4. **Robustness**: Comprehensive error handling and edge case management
5. **Testability**: Well-tested with extensive unit test coverage

### Class Relationships

```
ArgParse
├── User-defined parsers (inherit from ArgParse)
├── Command handlers (methods in subclasses)
└── Argument specifications (dictionaries)

Hostfile
├── Pattern expansion engine
├── IP resolution system
└── Host manipulation operations
```

### Dependencies

- **Standard Library**: `socket`, `re`, `os`, `ast`, `typing`
- **Testing**: `unittest`, `tempfile`
- **No External Dependencies**: Both classes use only Python standard library

## File Structure

```
jarvis_cd/
├── util/
│   ├── __init__.py
│   ├── argparse.py       # ArgParse class implementation
│   └── hostfile.py       # Hostfile class implementation
├── test/
│   └── unit/
│       ├── test_argparse.py   # ArgParse unit tests
│       └── test_hostfile.py   # Hostfile unit tests
└── docs/
    ├── README.md         # This overview document
    ├── argparse.md       # Detailed ArgParse documentation
    └── hostfile.md       # Detailed Hostfile documentation
```

## Best Practices

### For ArgParse

1. **Define clear command hierarchies** with logical menu organization
2. **Use argument classes and ranks** for intuitive positional ordering
3. **Provide meaningful aliases** for frequently used commands
4. **Implement robust error handling** in command methods
5. **Test complex argument combinations** thoroughly

### For Hostfile

1. **Use pattern expansion** to minimize hostfile maintenance
2. **Disable IP resolution** for large host lists when not needed
3. **Test patterns** with small examples before large deployments
4. **Handle file not found** gracefully in applications
5. **Use `is_local()`** to detect single-machine vs. distributed scenarios

### For Integration

1. **Combine both classes** for comprehensive CLI applications
2. **Validate hostfile patterns** before expensive operations
3. **Use subset operations** for testing and development
4. **Cache hostfile objects** for repeated use
5. **Document command structures** clearly for users

## Future Extensions

Potential areas for enhancement:

1. **ArgParse**: Configuration file support, command completion, help generation
2. **Hostfile**: SSH key management, health checking, load balancing hints
3. **Integration**: Plugin system, workflow orchestration, monitoring hooks

## Contributing

When extending these classes:

1. **Maintain backward compatibility** in public APIs
2. **Add comprehensive tests** for new functionality
3. **Update documentation** with examples and use cases
4. **Follow existing code style** and patterns
5. **Consider performance impact** of changes

---

For detailed API documentation and examples, see the individual class documentation:
- [ArgParse Class Documentation](./argparse.md)
- [Hostfile Class Documentation](./hostfile.md)
```

### `test/README.md`

```markdown
# Jarvis CD Test Suite

Comprehensive unit tests for the Jarvis CD project, organized into three main categories:
- **core**: Tests for CLI commands and core functionality
- **shell**: Tests for execution modules (LocalExec, SshExec, etc.)
- **util**: Tests for utility modules (argparse, hostfile, etc.)

## Test Structure

```
test/
├── unit/
│   ├── core/          # CLI command tests
│   │   ├── test_cli_base.py
│   │   ├── test_cli_init.py
│   │   ├── test_cli_pipeline.py
│   │   ├── test_cli_repo_pkg.py
│   │   └── test_cli_env_rg.py
│   ├── shell/         # Execution module tests
│   │   ├── test_local_exec.py
│   │   ├── test_ssh_exec.py
│   │   ├── test_scp_exec.py
│   │   ├── test_mpi_exec.py
│   │   └── test_env_forwarding.py
│   └── util/          # Utility module tests
│       ├── test_argparse.py
│       ├── test_argparse_comprehensive.py
│       └── test_hostfile.py
├── Dockerfile         # Docker container for isolated testing
├── docker-compose.yml # Docker Compose configuration
├── run_tests.sh       # Test runner script
└── README.md          # This file
```

## Running Tests

### Option 1: Using Docker (Recommended)

Docker provides an isolated environment that won't affect your host system.

**Run all tests:**
```bash
./test/run_tests.sh all
```

**Run specific test suites:**
```bash
./test/run_tests.sh shell    # Shell module tests only
./test/run_tests.sh util     # Utility module tests only
./test/run_tests.sh core     # Core CLI tests only
./test/run_tests.sh parallel # All tests in parallel
```

**Pass additional pytest arguments:**
```bash
./test/run_tests.sh all -v --tb=short
./test/run_tests.sh shell -k test_local
./test/run_tests.sh parallel -n 4
```

### Option 2: Using Docker Compose Directly

```bash
cd test/

# Run all tests
docker-compose run --rm test

# Run specific test suite
docker-compose run --rm test-shell
docker-compose run --rm test-util
docker-compose run --rm test-core

# Run tests in parallel
docker-compose run --rm test-parallel
```

### Option 3: Local Python Environment

If you prefer to run tests locally (not containerized):

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-xdist

# Run all tests
python -m pytest test/unit/ -v

# Run specific test directory
python -m pytest test/unit/shell/ -v
python -m pytest test/unit/util/ -v
python -m pytest test/unit/core/ -v

# Run with coverage
python -m pytest test/unit/ --cov=jarvis_cd --cov-report=term-missing --cov-report=html

# Run tests in parallel
python -m pytest test/unit/ -n auto
```

## Test Categories

### Core Tests (test/unit/core/)

Tests for CLI commands and core functionality:

- **test_cli_init.py**: `jarvis init` command
- **test_cli_pipeline.py**: `jarvis ppl` commands (create, append, run, start, stop, etc.)
- **test_cli_repo_pkg.py**: `jarvis repo` and `jarvis pkg` commands
- **test_cli_env_rg.py**: Environment, resource graph, module, and hostfile commands

**Key Features Tested:**
- Command parsing and argument validation
- Default values and required arguments
- Command aliases
- Error handling

### Shell Tests (test/unit/shell/)

Tests for execution modules:

- **test_local_exec.py**: LocalExec execution and environment handling
- **test_ssh_exec.py**: SSH/PSSH remote execution
- **test_scp_exec.py**: SCP/PSCP file transfer
- **test_mpi_exec.py**: MPI parallel execution
- **test_env_forwarding.py**: Environment variable forwarding across all exec types

**Key Features Tested:**
- Environment variable forwarding and type conversion
- Command construction and escaping
- Output collection and piping
- Async execution
- Error handling and exit codes

### Util Tests (test/unit/util/)

Tests for utility modules:

- **test_argparse.py**: Basic argument parsing
- **test_argparse_comprehensive.py**: Comprehensive argparse testing
- **test_hostfile.py**: Hostfile parsing and management

**Key Features Tested:**
- Type conversions (int, float, str, bool, list, dict)
- Required arguments and defaults
- Positional and keyword arguments
- Boolean flags (+/-)
- Choices validation
- Remainder arguments

## Code Coverage

After running tests with coverage, view the HTML report:

```bash
# Coverage report is generated in htmlcov/
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Current Coverage Targets:**
- Shell modules: 70-100% coverage
- Util modules: 70-90% coverage
- Core modules: Initial coverage being established

## Writing New Tests

### Adding CLI Command Tests

1. Create a new test file in `test/unit/core/`
2. Inherit from `CLITestBase` for common utilities
3. Use helper methods like `run_command()`, `create_test_pipeline()`, etc.

Example:
```python
from test_cli_base import CLITestBase

class TestMyCLICommand(CLITestBase):
    def test_my_command(self):
        args = ['my', 'command', 'arg1']
        result = self.run_command(args)
        self.assertTrue(result.get('success'))
        self.assertEqual(result['kwargs']['arg_name'], 'arg1')
```

### Adding Shell Tests

1. Create tests in `test/unit/shell/`
2. Test execution, environment variables, and output handling
3. Use cross-platform Python scripts for verification

### Adding Util Tests

1. Create tests in `test/unit/util/`
2. Focus on API correctness and type conversions
3. Test edge cases and error conditions

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests in Docker
  run: ./test/run_tests.sh all

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./htmlcov/coverage.xml
```

## Troubleshooting

### Docker Issues

**Problem**: Docker build fails
```bash
# Clean Docker cache and rebuild
docker system prune -a
cd test && docker-compose build --no-cache
```

**Problem**: Permission denied
```bash
# Ensure run_tests.sh is executable
chmod +x test/run_tests.sh
```

### Test Failures

**Problem**: SSH/SCP tests fail
- Expected behavior: Some tests use mock hostnames that won't resolve
- These failures are normal in isolated environments

**Problem**: MPI tests skipped
- Expected behavior: MPI tests skip when OpenMPI is not installed
- Use Docker environment for full MPI test coverage

### Coverage Issues

**Problem**: Coverage report not generated
```bash
# Ensure pytest-cov is installed
pip install pytest-cov

# Generate coverage explicitly
python -m pytest test/unit/ --cov=jarvis_cd --cov-report=html
```

## Best Practices

1. **Isolation**: Tests should not depend on external state
2. **Cleanup**: Use setUp/tearDown to manage test resources
3. **Assertions**: Be specific with assertions (assertEqual vs assertTrue)
4. **Documentation**: Add docstrings to test methods
5. **Naming**: Use descriptive test names (test_feature_scenario)

## Contributing

When adding new features to Jarvis CD:

1. Write tests first (TDD approach recommended)
2. Ensure tests pass locally
3. Run full test suite in Docker before submitting PR
4. Aim for 80%+ coverage on new code
5. Update this README if adding new test categories

## Support

For questions or issues with the test suite:
- Check existing tests for examples
- Review pytest documentation: https://docs.pytest.org/
- Open an issue in the project repository
```

### `.gitignore`

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
.idea
/config
jarvis_repos
jarvis_envs
.jarvis_env
hostfile.txt

.env*

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
/.idea/jarvis-cd.iml
/.idea/misc.xml
/.idea/modules.xml
/.idea/inspectionProfiles/profiles_settings.xml
/.idea/inspectionProfiles/Project_Default.xml
/.idea/vcs.xml
/.idea/deployment.xml
```

### `LICENSE`

```
# BSD 3-Clause License

Copyright (c) 2024, Gnosis Research Center, Illinois Institute of Technology
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---

**Contact Information:**
Gnosis Research Center  
Illinois Institute of Technology  
Email: grc@illinoistech.edu
```

### `builtin/builtin/orangefs/Dockerfile`

```dockerfile
FROM iowarp/iowarp-build:latest

# Set non-interactive frontend to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone to avoid prompt during package installation
ENV TZ=Etc/UTC

# Update package lists
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Reset frontend
ENV DEBIAN_FRONTEND=dialog

# SCSPKG + lmod
RUN echo $'\n\
    if ! shopt -q login_shell; then\n\
    if [ -d /etc/profile.d ]; then\n\
    for i in /etc/profile.d/*.sh; do\n\
    if [ -r $i ]; then\n\
    . $i\n\
    fi\n\
    done\n\
    fi\n\
    fi\n\
    ' >> /root/.bashrc
RUN . "${SPACK_DIR}/share/spack/setup-env.sh" && \
    spack load iowarp && \
    echo "module use $(scspkg module dir)" >> /root/.bashrc && \
    scspkg init tcl

# Install OFS dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y automake bison flex \
    libdb-dev \
    libsqlite3-dev libfuse-dev fuse

# Install libfuse
RUN . "${SPACK_DIR}/share/spack/setup-env.sh" && \
    spack install libfuse@2.9

# Install OFS
RUN . "${SPACK_DIR}/share/spack/setup-env.sh" && \
    spack load iowarp libfuse && \
    scspkg create orangefs && \
    cd $(scspkg pkg src orangefs) && \
    wget https://github.com/waltligon/orangefs/releases/download/v.2.10.0/orangefs-2.10.0.tar.gz && \
    tar -xvzf orangefs-2.10.0.tar.gz && \
    cd orangefs && \
    ./prepare && \
    ./configure --prefix=$(scspkg pkg root orangefs) --enable-shared --enable-fuse && \
    make -j8 && \
    make install && \
    scspkg env prepend orangefs ORANGEFS_PATH $(scspkg pkg root orangefs)

# Install OFS with openmpi
```

### `pyproject.toml`

```toml
[project]
name = "jarvis_cd"
description = "Jarvis-CD: Unified platform for deploying applications and benchmarks"
readme = "README.md"
requires-python = ">=3.7"
dynamic = ["version"]
authors = [
  {name = "Luke Logan", email = "llogan@hawk.iit.edu"},
]
classifiers = [
  "Programming Language :: Python",
  "Programming Language :: Python :: 3",
  "Development Status :: 4 - Beta",
  "Environment :: Console",
  "Intended Audience :: Developers",
  "Intended Audience :: System Administrators",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "Topic :: System :: Systems Administration",
  "Topic :: System :: Distributed Computing",
]
dependencies = [
  "pyyaml",
  "pandas",
  "podman-compose",
]

[project.urls]
Documentation = "https://github.com/iowarp/ppi-jarvis-cd"
issue-tracker = "https://github.com/iowarp/ppi-jarvis-cd/issues"
source-code = "https://github.com/iowarp/ppi-jarvis-cd"

[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools>=42",
  "setuptools-scm>=7",
]

[tool.setuptools]
packages = ["jarvis_cd", "jarvis_cd.core", "jarvis_cd.shell", "jarvis_cd.util", "builtin", "builtin.builtin"]
include-package-data = true

[tool.setuptools.package-data]
jarvis_cd = ["*.yaml", "*.yml"]
"*" = ["*.py", "*.yaml", "*.yml", "*.md", "*.txt", "*.conf", "*.xml", "*.param", "*.f", "*.input", "*.png", "*.sh"]
builtin = ["pipelines/**/*.yaml", "pipelines/**/*.yml"]

[project.scripts]
jarvis = "jarvis_cd.core.cli:main"

[tool.setuptools_scm]
version_scheme = "no-guess-dev"
```

### `requirements.txt`

```
pyyaml
#pylint==2.15.0
#coverage==5.5
#coverage-lcov==0.2.4
#pytest==6.2.5
```

### `setup.py`

```python
import setuptools

# Use setup() with minimal configuration since pyproject.toml handles most metadata
setuptools.setup(
    scripts=['bin/jarvis', 'bin/jarvis_resource_graph'],
)

# Install builtin packages immediately after setup
try:
    from jarvis_cd.post_install import install_builtin_packages
    install_builtin_packages()
except Exception as e:
    print(f"Warning: Could not install builtin packages: {e}")
```

### `test/Dockerfile`

```dockerfile
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gcc \
    g++ \
    make \
    git \
    openssh-client \
    openssh-server \
    rsync \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install MPI for MPI tests (optional)
RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libopenmpi-dev \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH server
RUN mkdir -p /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create test user
RUN useradd -m -s /bin/bash testuser && \
    echo "testuser:testpass" | chpasswd && \
    usermod -aG sudo testuser

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Install test dependencies
RUN pip3 install --no-cache-dir \
    pytest>=8.0.0 \
    pytest-cov>=4.0.0 \
    pytest-xdist>=3.0.0 \
    coverage>=7.0.0

# Copy the entire project
COPY . /app/

# Compile test binaries
RUN gcc /app/test/unit/shell/test_env_checker.c -o /app/test/unit/shell/test_env_checker

# Set up SSH keys for testuser (passwordless SSH to localhost)
RUN mkdir -p /home/testuser/.ssh && \
    ssh-keygen -t rsa -N "" -f /home/testuser/.ssh/id_rsa && \
    cat /home/testuser/.ssh/id_rsa.pub >> /home/testuser/.ssh/authorized_keys && \
    chmod 700 /home/testuser/.ssh && \
    chmod 600 /home/testuser/.ssh/authorized_keys && \
    chmod 600 /home/testuser/.ssh/id_rsa && \
    chown -R testuser:testuser /home/testuser/.ssh

# Configure SSH client for testuser
RUN echo "Host localhost" >> /home/testuser/.ssh/config && \
    echo "    StrictHostKeyChecking no" >> /home/testuser/.ssh/config && \
    echo "    UserKnownHostsFile=/dev/null" >> /home/testuser/.ssh/config && \
    chmod 600 /home/testuser/.ssh/config && \
    chown testuser:testuser /home/testuser/.ssh/config

# Change ownership to test user
RUN chown -R testuser:testuser /app

# Switch to test user
USER testuser

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Create entrypoint script to start SSH daemon
USER root
RUN echo '#!/bin/bash\n\
# Start SSH daemon\n\
sudo /usr/sbin/sshd\n\
# Wait for SSH to be ready\n\
sleep 2\n\
# Execute the command passed to the container\n\
exec "$@"\n\
' > /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown testuser:testuser /entrypoint.sh

# Allow testuser to run sshd without password
RUN echo "testuser ALL=(ALL) NOPASSWD: /usr/sbin/sshd" >> /etc/sudoers

USER testuser

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command runs all tests
CMD ["python3", "-m", "pytest", "test/unit/", "-v", "--cov=jarvis_cd", "--cov-report=term-missing", "--cov-report=html:/app/htmlcov"]
```

### `test/docker-compose.yml`

```yaml
version: '3.8'

services:
  # Main test service
  test:
    build:
      context: ..
      dockerfile: test/Dockerfile
    volumes:
      - ../jarvis_cd:/app/jarvis_cd:ro
      - ../test:/app/test:ro
      - test-results:/app/htmlcov
    environment:
      - PYTHONPATH=/app
      - PYTEST_ARGS=${PYTEST_ARGS:-}
    command: >
      python3 -m pytest test/unit/ -v
      --cov=jarvis_cd
      --cov-report=term-missing
      --cov-report=html:/app/htmlcov
      ${PYTEST_ARGS}

  # Service for running only shell tests
  test-shell:
    build:
      context: ..
      dockerfile: test/Dockerfile
    volumes:
      - ../jarvis_cd:/app/jarvis_cd:ro
      - ../test:/app/test:ro
      - test-results:/app/htmlcov
    environment:
      - PYTHONPATH=/app
    command: >
      python3 -m pytest test/unit/shell/ -v
      --cov=jarvis_cd.shell
      --cov-report=term-missing

  # Service for running only util tests
  test-util:
    build:
      context: ..
      dockerfile: test/Dockerfile
    volumes:
      - ../jarvis_cd:/app/jarvis_cd:ro
      - ../test:/app/test:ro
      - test-results:/app/htmlcov
    environment:
      - PYTHONPATH=/app
    command: >
      python3 -m pytest test/unit/util/ -v
      --cov=jarvis_cd.util
      --cov-report=term-missing

  # Service for running only core tests
  test-core:
    build:
      context: ..
      dockerfile: test/Dockerfile
    volumes:
      - ../jarvis_cd:/app/jarvis_cd:ro
      - ../test:/app/test:ro
      - test-results:/app/htmlcov
    environment:
      - PYTHONPATH=/app
    command: >
      python3 -m pytest test/unit/core/ -v
      --cov=jarvis_cd.core
      --cov-report=term-missing

  # Service for running parallel tests
  test-parallel:
    build:
      context: ..
      dockerfile: test/Dockerfile
    volumes:
      - ../jarvis_cd:/app/jarvis_cd:ro
      - ../test:/app/test:ro
      - test-results:/app/htmlcov
    environment:
      - PYTHONPATH=/app
    command: >
      python3 -m pytest test/unit/ -v -n auto
      --cov=jarvis_cd
      --cov-report=term-missing
      --cov-report=html:/app/htmlcov

volumes:
  test-results:
```

### `.claude/agents/code-documenter.md`

```markdown
---
name: code-documenter
description: Use this agent when you need comprehensive documentation for code, APIs, or technical systems. Examples: <example>Context: User has just completed implementing a complex authentication system and needs documentation. user: 'I've finished building the OAuth2 authentication flow. Can you help document this?' assistant: 'I'll use the code-documenter agent to create comprehensive documentation for your OAuth2 implementation.' <commentary>Since the user needs detailed documentation for their code, use the code-documenter agent to analyze and document the authentication system.</commentary></example> <example>Context: User is working on a project and realizes their codebase lacks proper documentation. user: 'Our API endpoints are getting complex and we need better documentation for the team' assistant: 'Let me use the code-documenter agent to create detailed API documentation.' <commentary>The user needs comprehensive API documentation, so use the code-documenter agent to analyze and document the endpoints.</commentary></example>
model: opus
---

You are an expert technical documentation specialist with deep expertise in code analysis, API documentation, and technical writing. Your mission is to create comprehensive, accurate, and developer-friendly documentation that makes complex code accessible and maintainable.

Your core responsibilities:
- Analyze code structure, functionality, and dependencies to understand the complete system
- Create detailed documentation that covers purpose, usage, parameters, return values, and examples
- Document APIs with clear endpoint descriptions, request/response formats, and authentication requirements
- Explain complex algorithms and business logic in clear, understandable terms
- Identify and document edge cases, error conditions, and troubleshooting guidance
- Ensure documentation follows established standards and best practices for the technology stack

Your documentation approach:
1. **Analysis First**: Thoroughly examine the code to understand its purpose, dependencies, and integration points
2. **Structure Logically**: Organize documentation in a logical flow from overview to detailed implementation
3. **Include Examples**: Provide practical code examples and usage scenarios for all documented features
4. **Be Comprehensive**: Cover all public interfaces, configuration options, and important implementation details
5. **Stay Current**: Ensure documentation accurately reflects the current code state

Documentation standards you follow:
- Use clear, concise language appropriate for the target audience
- Include code examples that are tested and functional
- Provide both high-level overviews and detailed technical specifications
- Document error conditions and exception handling
- Include setup, configuration, and deployment instructions when relevant
- Cross-reference related components and dependencies

When creating documentation:
- Start with a clear purpose statement and overview
- Document all public methods, classes, and interfaces
- Explain complex business logic and algorithms
- Include parameter types, constraints, and validation rules
- Provide return value descriptions and possible error conditions
- Add usage examples for common scenarios
- Note any breaking changes or version compatibility issues

Always ask for clarification if the code's purpose or intended audience is unclear. Your documentation should enable other developers to understand, use, and maintain the code effectively.
```

### `.claude/agents/docker-python-test-expert.md`

```markdown
---
name: docker-python-test-expert
description: Use this agent when you need to write Python unit tests for Dockerized applications, create Docker configurations for test environments, debug Docker-related test failures, set up test containers, or optimize testing workflows in containerized Python projects. Examples: (1) User: 'I need to write unit tests for this Flask API that runs in Docker' → Assistant: 'I'm going to use the docker-python-test-expert agent to create comprehensive unit tests for your Dockerized Flask API' (2) User: 'My pytest suite fails in Docker but works locally' → Assistant: 'Let me use the docker-python-test-expert agent to diagnose and fix the Docker-specific test failures' (3) User: 'How do I set up a test database container for my Python tests?' → Assistant: 'I'll use the docker-python-test-expert agent to configure a proper test database container setup'
model: sonnet
---

You are an elite Docker and Python testing specialist with deep expertise in containerized application testing, test-driven development, and CI/CD pipelines. You combine mastery of Docker containerization with advanced Python testing frameworks to create robust, reliable test suites.

Your core responsibilities:

1. **Python Unit Testing Excellence**:
   - Write comprehensive unit tests using pytest, unittest, or other appropriate frameworks
   - Implement proper test isolation, mocking, and fixture management
   - Follow testing best practices: AAA pattern (Arrange-Act-Assert), clear test naming, single responsibility
   - Create parameterized tests for edge cases and boundary conditions
   - Ensure high code coverage while focusing on meaningful test scenarios
   - Use appropriate assertion libraries and custom matchers when needed

2. **Docker Testing Integration**:
   - Design Docker Compose configurations for test environments
   - Set up test containers for databases, message queues, and external services
   - Implement proper container lifecycle management in tests (setup/teardown)
   - Configure volume mounts and networking for test isolation
   - Optimize Docker layer caching for faster test execution
   - Handle environment-specific configurations and secrets securely

3. **Test Environment Architecture**:
   - Create reproducible test environments using Docker
   - Implement test data seeding and cleanup strategies
   - Configure health checks and wait strategies for dependent services
   - Set up multi-stage Docker builds separating test and production dependencies
   - Design efficient test execution workflows (parallel execution, test ordering)

4. **Debugging and Troubleshooting**:
   - Diagnose Docker-specific test failures (networking, volumes, permissions)
   - Identify and resolve race conditions in containerized tests
   - Debug container logs and test output effectively
   - Handle platform-specific issues (Linux vs macOS vs Windows)

5. **Quality Assurance**:
   - Verify tests are deterministic and don't have hidden dependencies
   - Ensure proper cleanup of Docker resources after test runs
   - Validate test performance and identify bottlenecks
   - Check for test flakiness and implement retry mechanisms when appropriate

When writing tests:
- Always consider the Docker context and potential containerization issues
- Use testcontainers-python or similar libraries when appropriate
- Implement proper async/await patterns for async Python code
- Include integration tests that verify Docker networking and service communication
- Document any Docker-specific setup requirements or gotchas
- Provide clear error messages and debugging hints in test failures

When encountering ambiguity:
- Ask about the specific Python version and testing framework preferences
- Clarify the Docker base images and service dependencies
- Confirm whether tests should run in CI/CD and what platform
- Verify if there are existing testing patterns or conventions to follow

Your output should include:
- Well-structured, maintainable test code with clear documentation
- Docker configuration files (Dockerfile, docker-compose.yml) when needed
- Setup instructions for running tests locally and in CI/CD
- Explanations of testing strategies and architectural decisions

Always prioritize test reliability, maintainability, and execution speed while ensuring comprehensive coverage of critical functionality.
```

### `.claude/agents/git-expert.md`

```markdown
---
name: git-expert
description: Use this agent when you need to perform git operations, manage repositories, work with submodules, commit code changes, analyze diffs, generate commit messages, or interact with GitHub APIs. Examples:\n\n<example>\nContext: User has made code changes and wants to commit them with an appropriate message.\nuser: "I've finished implementing the authentication feature. Can you commit these changes?"\nassistant: "Let me use the git-expert agent to analyze the changes and create an appropriate commit."\n<commentary>The user wants to commit code changes. Use the Task tool to launch the git-expert agent to handle the git operations.</commentary>\n</example>\n\n<example>\nContext: User needs to update submodules in their repository.\nuser: "The submodules are out of sync. Can you update them recursively?"\nassistant: "I'll use the git-expert agent to recursively update all submodules."\n<commentary>The user needs submodule management. Use the git-expert agent to handle recursive submodule operations.</commentary>\n</example>\n\n<example>\nContext: User wants to understand what changed in recent commits.\nuser: "What changed in the last commit?"\nassistant: "Let me use the git-expert agent to analyze the git diff and describe the changes."\n<commentary>The user wants to understand code changes. Use the git-expert agent to analyze diffs and provide clear descriptions.</commentary>\n</example>\n\n<example>\nContext: Proactive use after code modifications are complete.\nuser: "I've updated the API endpoints and added error handling."\nassistant: "Great work! Let me use the git-expert agent to review the changes and prepare a commit."\n<commentary>Code changes have been made. Proactively use the git-expert agent to handle version control operations.</commentary>\n</example>
tools: Bash, Glob, Grep, Read, WebFetch, TodoWrite, WebSearch, BashOutput, KillShell
model: haiku
---

You are an elite Git and GitHub operations specialist with deep expertise in version control workflows, repository management, and GitHub API integration. Your role is to handle all git-related operations with precision and best practices.

## Core Responsibilities

1. **Git Operations**: Execute git commands efficiently and safely, including commits, branches, merges, rebases, and tags. Always verify the current repository state before performing destructive operations.

2. **Submodule Management**: Handle recursive submodule operations with expertise. When updating submodules, always use `git submodule update --init --recursive` to ensure all nested submodules are properly initialized and updated.

3. **Commit Management**: 
   - Analyze git diffs to understand the scope and nature of changes
   - Generate clear, descriptive commit messages following conventional commit format when appropriate
   - Structure commits logically, grouping related changes
   - Use imperative mood in commit messages (e.g., "Add feature" not "Added feature")
   - Include context about why changes were made, not just what changed

4. **Change Analysis**: When examining diffs:
   - Identify the files modified, added, or deleted
   - Summarize the functional impact of changes
   - Highlight potential breaking changes or important modifications
   - Provide context about the scope (e.g., "refactoring", "bug fix", "new feature")

5. **GitHub API Integration**: Leverage GitHub APIs for:
   - Creating and managing pull requests
   - Reviewing repository information
   - Managing issues and labels
   - Accessing repository metadata

## Operational Guidelines

- **Safety First**: Before executing potentially destructive operations (reset, force push, etc.), clearly explain the implications and confirm intent
- **Status Checks**: Always check repository status before major operations using `git status`
- **Branch Awareness**: Be conscious of the current branch and working directory state
- **Conflict Resolution**: When conflicts arise, provide clear guidance on resolution strategies
- **Clean History**: Encourage atomic commits and clean commit history practices

## Best Practices

- Use `git diff --staged` to review changes before committing
- Prefer `git pull --rebase` to maintain linear history when appropriate
- When working with submodules, always verify their state after updates
- For commit messages: use a clear subject line (50 chars or less), followed by a blank line and detailed body if needed
- Leverage `git log --oneline --graph` for visualizing branch history

## Error Handling

- If a git command fails, analyze the error message and provide actionable solutions
- For merge conflicts, guide through the resolution process step-by-step
- If repository state is unclear, use diagnostic commands to gather information before proceeding

## Output Format

- When describing changes, structure your response with clear sections: files changed, summary of modifications, and recommended commit message
- For command execution, show the command being run and explain its purpose
- When analyzing diffs, present information in a hierarchical format: high-level summary, then file-by-file details if needed

You have the authority to execute git commands directly but should explain your actions clearly. When uncertain about the user's intent or when operations could have significant consequences, ask for clarification before proceeding.
```

### `.claude/agents/jarvis-pipeline-builder.md`

```markdown
---
name: jarvis-pipeline-builder
description: Use this agent when the user needs to create, modify, or understand Jarvis pipeline YAML files, or when they need to extract and document parameters from pipeline packages. Examples:\n\n<example>\nContext: User is working on creating a new pipeline configuration.\nuser: "I need to create a pipeline YAML for processing data through the ETL workflow"\nassistant: "I'm going to use the Task tool to launch the jarvis-pipeline-builder agent to help you create the pipeline YAML configuration."\n<commentary>\nThe user needs pipeline YAML creation assistance, which is the core expertise of the jarvis-pipeline-builder agent.\n</commentary>\n</example>\n\n<example>\nContext: User has just written code for a new pipeline package.\nuser: "I've just finished implementing the DataTransformer package. Can you help me understand what parameters it needs?"\nassistant: "I'm going to use the Task tool to launch the jarvis-pipeline-builder agent to analyze the DataTransformer package and extract its parameters."\n<commentary>\nThe user needs to understand package parameters, which requires the jarvis-pipeline-builder agent's expertise in reading packages and their parameter structures.\n</commentary>\n</example>\n\n<example>\nContext: User is reviewing existing pipeline configurations.\nuser: "Can you review this pipeline YAML and tell me if the parameters are correctly configured?"\nassistant: "I'm going to use the Task tool to launch the jarvis-pipeline-builder agent to review the pipeline YAML configuration and validate the parameters."\n<commentary>\nThe user needs expert review of pipeline YAML structure and parameter configuration.\n</commentary>\n</example>
model: sonnet
---

You are an elite Jarvis pipeline architect with deep expertise in constructing, analyzing, and optimizing Jarvis pipeline YAML configurations. Your specialized knowledge encompasses both the YAML structure and the underlying package implementations that power these pipelines.

## Core Responsibilities

You will:
- Design and construct well-structured Jarvis pipeline YAML files that follow best practices
- Analyze package source code to extract accurate parameter specifications, types, defaults, and constraints
- Validate pipeline configurations for correctness, completeness, and efficiency
- Troubleshoot pipeline configuration issues and suggest optimizations
- Document parameter requirements clearly and comprehensively

## Operational Guidelines

### When Building Pipeline YAML Files:
1. **Structure First**: Ensure proper YAML syntax and hierarchical organization
2. **Parameter Accuracy**: Cross-reference package implementations to verify all required parameters are included with correct types and formats
3. **Defaults and Optionals**: Clearly distinguish between required parameters and those with defaults
4. **Validation**: Include appropriate validation rules and constraints where applicable
5. **Documentation**: Add inline comments explaining non-obvious configuration choices
6. **Dependencies**: Ensure proper ordering and dependency management between pipeline stages

### When Reading Package Parameters:
1. **Thorough Analysis**: Examine package constructors, configuration classes, and parameter validation logic
2. **Type Extraction**: Identify precise parameter types (string, int, float, bool, list, dict, etc.)
3. **Constraint Discovery**: Note any validation rules, allowed values, ranges, or format requirements
4. **Default Values**: Document default values when they exist
5. **Required vs Optional**: Clearly distinguish mandatory parameters from optional ones
6. **Nested Structures**: Handle complex nested parameter structures accurately

### Quality Assurance:
- Always verify parameter names match exactly as defined in the package code
- Check for deprecated parameters or configuration patterns
- Ensure YAML syntax is valid and properly indented
- Validate that parameter types in YAML align with package expectations
- Consider edge cases and potential configuration conflicts

### When Uncertain:
- If package code is ambiguous, examine usage examples or tests
- If parameter requirements are unclear, ask for clarification rather than guessing
- If multiple valid approaches exist, present options with trade-offs

### Output Format:
- For YAML files: Provide complete, valid YAML with clear structure and helpful comments
- For parameter documentation: Use structured format showing name, type, required/optional status, default value (if any), description, and constraints
- For analysis: Provide clear, actionable insights with specific references to code locations when relevant

## Best Practices:
- Maintain consistency in naming conventions and structure across pipeline stages
- Optimize for readability and maintainability
- Include error handling and fallback configurations where appropriate
- Consider performance implications of configuration choices
- Follow any project-specific patterns established in existing pipeline files

You approach each task methodically, ensuring accuracy and completeness while maintaining clarity in your explanations and configurations.
```

### `.claude/agents/python-code-updater.md`

```markdown
---
name: python-code-updater
description: Use this agent when you need to modify, refactor, or enhance existing Python code. This includes updating deprecated syntax, improving performance, adding new features to existing functions/classes, fixing bugs, modernizing code to newer Python versions, or restructuring code for better maintainability. Examples: <example>Context: User has existing Python code that needs to be updated to use newer syntax or libraries. user: 'Can you update this function to use f-strings instead of .format()?' assistant: 'I'll use the python-code-updater agent to modernize this code with f-string syntax.' <commentary>The user wants to update existing Python code with modern syntax, which is exactly what the python-code-updater agent specializes in.</commentary></example> <example>Context: User has a Python script that needs performance improvements. user: 'This loop is running slowly, can you optimize it?' assistant: 'Let me use the python-code-updater agent to analyze and optimize this code for better performance.' <commentary>The user needs existing code improved for performance, which falls under the python-code-updater's expertise in enhancing existing Python code.</commentary></example>
model: sonnet
---

You are a professional software engineer specializing in Python code updates and improvements. You excel at analyzing existing Python code and making targeted enhancements while preserving functionality and improving code quality.

Your core responsibilities:
- Analyze existing Python code to understand its current functionality and structure
- Identify opportunities for improvement including performance, readability, maintainability, and modern Python practices
- Update code using current Python best practices and idioms
- Ensure backward compatibility when possible, or clearly communicate breaking changes
- Maintain existing functionality while enhancing code quality
- Follow PEP 8 style guidelines and modern Python conventions

Your approach:
1. First, thoroughly understand the existing code's purpose and current implementation
2. Identify specific areas for improvement (performance bottlenecks, deprecated syntax, code smells, etc.)
3. Plan updates that maintain functionality while improving code quality
4. Implement changes incrementally, testing logic as you go
5. Provide clear explanations of what was changed and why
6. Highlight any potential impacts or considerations for the updates

Key principles:
- Always preserve the original functionality unless explicitly asked to change behavior
- Use modern Python features appropriately (f-strings, type hints, dataclasses, etc.)
- Optimize for readability and maintainability over clever solutions
- Consider performance implications of your changes
- Follow established project patterns and conventions when evident
- Be explicit about any assumptions you make about the code's usage

When updating code:
- Explain your reasoning for each significant change
- Point out any potential breaking changes or migration considerations
- Suggest additional improvements that might be beneficial
- Ensure error handling is appropriate and robust
- Consider edge cases that might not be handled in the original code

You should ask for clarification if the update requirements are ambiguous or if there are multiple valid approaches to improving the code.
```

### `.github/workflows/build-containers.yaml`

```yaml
name: Build Containers

on:
  workflow_dispatch:
  workflow_call:

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 800

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        id: buildx

      - name: Build and push build image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./docker/build.Dockerfile
          builder: ${{ steps.buildx.outputs.name }}
          platforms: linux/amd64,linux/arm64
          push: true
          tags: iowarp/ppi-jarvis-cd-build:latest

      - name: Build and push deploy image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./docker/deploy.Dockerfile
          builder: ${{ steps.buildx.outputs.name }}
          platforms: linux/amd64,linux/arm64
          push: true
          tags: iowarp/ppi-jarvis-cd:latest
```

### `.github/workflows/main.yml`

```yaml
name: main

on:
  # push:
  # pull_request:
  #   branches: [ main ]
  workflow_dispatch:
    inputs:
      debug_enabled:
        description: 'Run the build with tmate debugging enabled'
        required: false
        default: false
env:
  BUILD_TYPE: Debug
  LOCAL: local

jobs:
  build:
    runs-on: ubuntu-24.04

    steps:
      - name: Get Sources
        uses: actions/checkout@v4

      - name: Install Apt Dependencies
        run: bash ci/install_deps.sh

      - name: Install Jarvis
        run: bash ci/install_jarvis.sh

      - name: Run pylint
        run: bash ci/lint.sh

      - name: Test
        run: bash ci/run_tests.sh

#      - name: Coveralls
#        uses: coverallsapp/github-action@master
#        with:
#          path-to-lcov: lcov.info
#          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### `.vscode/launch.json`

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug jarvis rg build",
            "type": "python",
            "python": "/home/llogan/.venv/bin/python",
            "request": "launch",
            "program": "/home/llogan/.venv/bin/jarvis",
            "args": [
                "ppl",
                "append",
                "chimaera_run"
            ],
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PATH": "/home/llogan/.scspkg/packages/iowarp_runtime/sbin:/home/llogan/.scspkg/packages/iowarp_runtime/bin:/usr/local/cuda/bin:/usr/local/cuda/gds/tools:/home/llogan/Documents/Projects/scspkg/packages/cuda/sbin:/home/llogan/Documents/Projects/scspkg/packages/cuda/bin:/opt/rocm/bin:/home/llogan/Documents/Projects/scspkg/packages/rocm/sbin:/home/llogan/Documents/Projects/scspkg/packages/rocm/bin:/home/llogan/.venv/bin:/home/llogan/.local/bin:/mnt/home/Projects/spack/bin:/home/llogan/.vscode-server/cli/servers/Stable-848b80aeb52026648a8ff9f7c45a9b0a80641e2e/server/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/llogan/.vscode-server/extensions/ms-python.debugpy-2025.8.0-linux-x64/bundled/scripts/noConfigScripts:/home/llogan/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand"
            }
        },
        {
            "name": "Debug jarvis ppl run",
            "type": "python",
            "python": "/home/llogan/.venv/bin/python",
            "request": "launch",
            "program": "/home/llogan/.venv/bin/jarvis",
            "args": [
                "ppl",
                "run"
            ],
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PATH": "/home/llogan/.scspkg/packages/iowarp_runtime/sbin:/home/llogan/.scspkg/packages/iowarp_runtime/bin:/usr/local/cuda/bin:/usr/local/cuda/gds/tools:/home/llogan/Documents/Projects/scspkg/packages/cuda/sbin:/home/llogan/Documents/Projects/scspkg/packages/cuda/bin:/opt/rocm/bin:/home/llogan/Documents/Projects/scspkg/packages/rocm/sbin:/home/llogan/Documents/Projects/scspkg/packages/rocm/bin:/home/llogan/.venv/bin:/home/llogan/.local/bin:/mnt/home/Projects/spack/bin:/home/llogan/.vscode-server/cli/servers/Stable-848b80aeb52026648a8ff9f7c45a9b0a80641e2e/server/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/llogan/.vscode-server/extensions/ms-python.debugpy-2025.8.0-linux-x64/bundled/scripts/noConfigScripts:/home/llogan/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand"
            }
        },
        {
            "name": "Debug jarvis ppl run with file",
            "type": "python",
            "python": "/home/llogan/.venv/bin/python",
            "request": "launch",
            "program": "/home/llogan/.venv/bin/jarvis",
            "args": [
                "ppl",
                "run",
                "builtin/pipelines/simple_test.yaml",
                "yaml"
            ],
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PATH": "/home/llogan/.scspkg/packages/iowarp_runtime/sbin:/home/llogan/.scspkg/packages/iowarp_runtime/bin:/usr/local/cuda/bin:/usr/local/cuda/gds/tools:/home/llogan/Documents/Projects/scspkg/packages/cuda/sbin:/home/llogan/Documents/Projects/scspkg/packages/cuda/bin:/opt/rocm/bin:/home/llogan/Documents/Projects/scspkg/packages/rocm/sbin:/home/llogan/Documents/Projects/scspkg/packages/rocm/bin:/home/llogan/.venv/bin:/home/llogan/.local/bin:/mnt/home/Projects/spack/bin:/home/llogan/.vscode-server/cli/servers/Stable-848b80aeb52026648a8ff9f7c45a9b0a80641e2e/server/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/llogan/.vscode-server/extensions/ms-python.debugpy-2025.8.0-linux-x64/bundled/scripts/noConfigScripts:/home/llogan/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand"
            }
        },
        {
            "name": "Debug jarvis ppl run (Python module)",
            "type": "python",
            "python": "/home/llogan/.venv/bin/python",
            "request": "launch",
            "module": "jarvis_cd.core.cli",
            "args": [
                "ppl",
                "run"
            ],
            "console": "integratedTerminal",
            "justMyCode": false,
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}",
                "PATH": "/home/llogan/.scspkg/packages/iowarp_runtime/sbin:/home/llogan/.scspkg/packages/iowarp_runtime/bin:/usr/local/cuda/bin:/usr/local/cuda/gds/tools:/home/llogan/Documents/Projects/scspkg/packages/cuda/sbin:/home/llogan/Documents/Projects/scspkg/packages/cuda/bin:/opt/rocm/bin:/home/llogan/Documents/Projects/scspkg/packages/rocm/sbin:/home/llogan/Documents/Projects/scspkg/packages/rocm/bin:/home/llogan/.venv/bin:/home/llogan/.local/bin:/mnt/home/Projects/spack/bin:/home/llogan/.vscode-server/cli/servers/Stable-848b80aeb52026648a8ff9f7c45a9b0a80641e2e/server/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/llogan/.vscode-server/extensions/ms-python.debugpy-2025.8.0-linux-x64/bundled/scripts/noConfigScripts:/home/llogan/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand"
            }
        }
    ]
}
```

### `CLAUDE.md`

```markdown
When adding new menus, create a new documentation file for describing the menu.

When adding new commands, make sure to document them under the docs directory. You should place the documentation in the doc file that is most relevant.
```

### `ai-prompts/docker/phase1.md`

```markdown
@CLAUDE.md 

Let's make two dockerfiles under the directory docker: 
build.Dockerfile and deploy.Dockerfile.

build and deploy should be built in the github actions. Manual only. Please edit the github actions. Add a new action called build_dockerfiles.yml

## build.Dockerfile

Pip install from workspace. Mount the parent directory as /workspace. 
Add to spack.

```Dockerfile
FROM iowarp/iowarp-deps:latest
LABEL maintainer="llogan@hawk.iit.edu"
LABEL version="0.0"
LABEL description="IOWarp ppi-jarvis-cd Docker image"

# Add ppi-jarvis-cd to Spack configuration
RUN echo "  py-ppi-jarvis-cd:" >> ~/.spack/packages.yaml && \
    echo "    externals:" >> ~/.spack/packages.yaml && \
    echo "    - spec: py-ppi-jarvis-cd" >> ~/.spack/packages.yaml && \
    echo "      prefix: /usr/local" >> ~/.spack/packages.yaml && \
    echo "    buildable: false" >> ~/.spack/packages.yaml

# Setup jarvis
RUN jarvis init
```

Also create a local.sh in docker directory to build the container locally. Should look something like this:
```bash
#!/bin/bash

# Build iowarp-runtime Docker image

# Get the project root directory (parent of docker folder)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/.." && pwd )"

echo $PROJECT_ROOT
echo $SCRIPT_DIR
# Build the Docker image
docker build  --no-cache -t iowarp/ppi-jarvis-cd-build:latest -f "${SCRIPT_DIR}/build.Dockerfile" "${PROJECT_ROOT}"
```

## deploy.Dockerfile

Essentially just does ``FROM iowarp/ppi-jarvis-cd-build:latest`` for now.

In the github action, create ``iowarp/ppi-jarvis-cd:latest``.
```

### `ai-prompts/new-pipeline.md`

```markdown
Use the python-code-updater agent to change the structure of pipleine scripts. 

The old format looked as follows
```python
name: chimaera_unit_ipc
env: chimaera
pkgs:
  - pkg_type: chimaera_run
    pkg_name: chimaera_run
    sleep: 10
    do_dbg: true
    dbg_port: 4000
  - pkg_type: chimaera_unit_tests
    pkg_name: chimaera_unit_tests
    TEST_CASE: TestBdevIo
    do_dbg: true
    dbg_port: 4001
```

The new format should look like this:
```python
name: chimaera_unit_ipc
env: chimaera
pkgs:
  - pkg_type: chimaera_run
    pkg_name: chimaera_run
    sleep: 10
    do_dbg: true
    dbg_port: 4000
  - pkg_type: chimaera_unit_tests
    pkg_name: chimaera_unit_tests
    TEST_CASE: TestBdevIo
    do_dbg: true
    dbg_port: 4001
    interceptors: hermes_api
interceptors:
  - pkg_type: hermes_api
    pkg_name: hermes_api
```

Here the "interceptors" keys ares the new thing. 

In the Package class, there should be a new function called add_interceptor. This should modify a new self.config key called 'interceptors'. The interceptors key will be similar to the sub_pkgs key. The set of interceptors should be stored in a dictionary. This dictionary should be a mapping of pkg_name to a constructed package.

In SimplePackage, add a new config parameter called "interceptors", which is a list of strings. The list parameters look like this:
```
 self.add_args([
            {
                'name': 'hosts',
                'msg': 'A list of hosts and threads pr',
                'type': list,
                'args': [
                    {
                        'name': 'host',
                        'msg': 'A string representing a host',
                        'type': str,
                    }
                ]
            }
        ])
```

When loading a SimplePackage, iterate over the set of strings there and check self.ppl for the interceptors. Call interceptor.modify_env() to update our environment. Remove the ability to pass mod_env to update_env function. Make it so mod_env is a copy (not pointer) to env. This way each package gets its own isolated module environment.
```

### `ai-prompts/phase-14-update.md`

```markdown
# Phase 14 Update - Recovered Changes

## Recovery Information

**Status:** ✅ RECOVERED - All lost commits have been saved to branch `recovery-phase-14`

**Recovery Date:** 2025-10-01
**Lost Commits Found:**
- `5775416` - Init jarvis repos (2025-09-30 16:53:03)
- `f8b3d6a` - Refactor resource graph and enhance module management (2025-10-01 11:34:50)

**To restore these changes:**
```bash
# Option 1: Merge into current branch
git merge recovery-phase-14

# Option 2: Cherry-pick specific commits
git cherry-pick 5775416 f8b3d6a

# Option 3: Checkout the recovery branch
git checkout recovery-phase-14
```

---

## Summary of Changes

This phase included major refactoring of the resource graph system, module management enhancements, CLI improvements, and extensive documentation updates across two commits.

### Files Changed (20 files total)
- **Added:** 1 file
- **Modified:** 18 files
- **Deleted:** 1 file
- **Net change:** +790 insertions, -264 deletions

---

## Commit 1: Init Jarvis Repos (5775416)

**Date:** 2025-09-30 16:53:03
**Files Changed:** 13 files

### Changes Made:

#### Removed Files
- **bin/jarvis-install-builtin** (128 lines deleted)
  - Removed legacy installation script

#### CLI Enhancements (jarvis_cd/core/cli.py)
- Added 80+ lines of new CLI functionality
- Enhanced command structure and argument parsing

#### Configuration Updates (jarvis_cd/core/config.py)
- Updated configuration handling (12 modifications)

#### Documentation Updates
- **docs/modules.md** (44 lines modified)
  - Updated module documentation with new patterns

- **docs/package_dev_guide.md** (2 modifications)
  - Updated development guide

- **docs/pipelines.md** (14 modifications)
  - Enhanced pipeline documentation

- **docs/resource_graph.md** (6 modifications)
  - Updated resource graph documentation

#### Other Updates
- **MANIFEST.in** - Updated manifest
- **ai-prompts/phase5-jarvis-repos.md** - Updated phase 5 documentation
- **jarvis_cd/core/module_manager.py** - Minor fix
- **jarvis_cd/core/resource_graph.py** - 12 modifications
- **pyproject.toml** - Updated project configuration
- **setup.py** - Simplified setup (11 lines removed)

---

## Commit 2: Refactor Resource Graph and Enhance Module Management (f8b3d6a)

**Date:** 2025-10-01 11:34:50
**Files Changed:** 15 files
**Impact:** +790 insertions, -264 deletions

This was the major refactoring commit with extensive changes across multiple subsystems.

---

### 1. Resource Graph System Refactoring

#### A. Core Architecture Changes (jarvis_cd/util/resource_graph.py)
**Major refactoring: 205 lines changed**

**Key Changes:**
- **Removed StorageDevice class** - Simplified to use plain Python dictionaries
- **Data model simplification:**
  ```python
  # OLD approach (class-based):
  device = StorageDevice(name, capacity, available)

  # NEW approach (dict-based):
  device = {
      'name': str,
      'capacity': int,
      'available': int
  }
  ```

- **Method renaming for clarity:**
  - `build_resource_graph()` → `build()`
  - `load_resource_graph()` → `load()`
  - `show_resource_graph()` → `show()`
  - `show_resource_graph_path()` → `show_path()`

- **Auto-loading on initialization:**
  - ResourceGraphManager now automatically loads the resource graph when instantiated
  - Eliminates need for separate initialization step

- **Display improvements:**
  - `show()` now displays raw YAML file instead of processed summary
  - Better debugging and verification of resource graph state

#### B. Binary Bug Fix (bin/jarvis_resource_graph)
**Critical fix: 7 lines modified**

- **Bug:** Available capacity was being overwritten with `None`
- **Impact:** Resource tracking was broken
- **Fix:** Corrected the capacity update logic to preserve available capacity

#### C. Resource Graph Manager (jarvis_cd/core/resource_graph.py)
**49 lines modified**

- Updated all method calls to use shortened names
- Improved error handling
- Enhanced integration with module system

#### D. Documentation (docs/resource_graph.md)
**100 lines reorganized**

Updated to reflect dictionary-based approach:
```yaml
# Example storage device structure
storage_devices:
  /path/to/storage:
    name: "storage_name"
    capacity: 1000000000  # bytes
    available: 500000000   # bytes
```

---

### 2. Module Management System Enhancements

#### A. New CLI Commands (jarvis_cd/core/cli.py)
**93 lines added**

**New Commands Implemented:**

1. **`jarvis mod clear`**
   - Cleans module directories while preserving src/ folder
   - Useful for resetting module state without losing source code
   - Safe cleanup operation

2. **`jarvis mod dep add <module> <dependency>`**
   - Adds dependencies to module configuration
   - Updates module metadata
   - Example: `jarvis mod dep add mymod hermes`

3. **`jarvis mod dep remove <module> <dependency>`**
   - Removes dependencies from module configuration
   - Cleans up module metadata
   - Example: `jarvis mod dep remove mymod hermes`

#### B. Module Manager Implementation (jarvis_cd/core/module_manager.py)
**133 lines added**

**New Methods:**
- `clear_module()` - Implementation of module clearing logic
- `add_dependency()` - Dependency addition logic
- `remove_dependency()` - Dependency removal logic
- Enhanced dependency tracking and validation
- Improved error messages

#### C. Module Documentation (docs/modules.md)
**63 lines added/modified**

**Documentation includes:**
- Usage examples for new commands
- Workflow patterns for module development
- Dependency management best practices
- Examples:
  ```bash
  # Clear a module (keeps src/)
  jarvis mod clear mymodule

  # Add dependency
  jarvis mod dep add mymodule hermes

  # Remove dependency
  jarvis mod dep remove mymodule hermes
  ```

---

### 3. Pipeline System Improvements

#### A. Pipeline Core (jarvis_cd/core/pipeline.py)
**131 lines modified (significant refactoring)**

**Key Improvements:**
- **Auto-configuration on load:**
  - Pipelines now automatically configure associated packages on load/update
  - Eliminates manual configuration step

- **Better integration with resource graph:**
  - Pipeline operations now respect resource graph constraints
  - Improved resource allocation and tracking

- **Enhanced error handling:**
  - More descriptive error messages
  - Better failure recovery

- **Workflow improvements:**
  - Streamlined pipeline creation and management
  - Better state tracking

#### B. Package Management (jarvis_cd/core/pkg.py)
**26 lines modified**

- Updated package configuration integration
- Improved auto-configuration logic
- Better package lifecycle management

---

### 4. Configuration System Updates

#### A. Config Core (jarvis_cd/core/config.py)
**45 lines modified**

**Improvements:**
- Enhanced configuration validation
- Better default value handling
- Improved configuration merging logic
- More robust error handling

#### B. Utility Functions (jarvis_cd/util/__init__.py)
**5 lines modified**

- Updated utility imports
- Better helper function organization
- Enhanced `load_class()` error messages

---

### 5. Shell and Process Management

#### A. Process Handling (jarvis_cd/shell/process.py)
**29 lines added**

**Enhancements:**
- Improved process spawning logic
- Better signal handling
- Enhanced subprocess management
- More robust error handling

---

### 6. Documentation Additions

#### A. New Agent Documentation (.claude/agents/git-expert.md)
**63 lines - NEW FILE**

Added Git expert agent configuration for Claude Code integration

#### B. Package Development Guide (docs/package_dev_guide.md)
**98 lines added**

**New sections:**
- **GdbServer Integration:**
  ```bash
  # Using GDB with Jarvis packages
  gdbserver :2000 ./my_package

  # Connect from GDB
  gdb ./my_package
  (gdb) target remote :2000
  ```

- **Debugging workflows**
- **Development best practices**
- **Testing strategies**

#### C. Pipeline Documentation (docs/pipelines.md)
**Updates to workflow examples**

- Enhanced pipeline configuration examples
- Better integration with resource graph
- Improved troubleshooting section

#### D. AI Prompt Documentation (ai-prompts/phase3-launch.md)
**7 lines added**

- Updated phase 3 documentation
- Added context for future development

---

## Key Architectural Improvements

### 1. Simplified Data Models
- Moved from class-based to dictionary-based storage devices
- Reduced code complexity
- Improved serialization/deserialization

### 2. Enhanced Developer Experience
- Shorter, more intuitive command names
- Auto-loading/auto-configuration reduces manual steps
- Better error messages throughout

### 3. Better Module Lifecycle Management
- Complete dependency management workflow
- Safe module cleanup operations
- Improved module state tracking

### 4. Resource Graph Reliability
- Fixed critical capacity tracking bug
- Improved resource allocation
- Better integration with pipelines

### 5. Documentation Quality
- Comprehensive examples throughout
- Real-world workflow patterns
- Developer-focused guidance

---

## Testing & Validation Notes

**Areas to test after merging:**

1. **Resource Graph:**
   - Verify capacity tracking works correctly
   - Test resource allocation in pipelines
   - Validate dictionary-based device access

2. **Module Management:**
   - Test `jarvis mod clear` preserves src/
   - Verify dependency add/remove operations
   - Check module configuration updates

3. **Pipeline Integration:**
   - Test auto-configuration on pipeline load
   - Verify package configuration workflow
   - Check resource graph integration

4. **CLI Commands:**
   - Test all new commands with various inputs
   - Verify error handling
   - Check help text accuracy

---

## Migration Notes

### Breaking Changes:
1. **ResourceGraphManager API:**
   - Old: `manager.build_resource_graph()`
   - New: `manager.build()`

2. **Storage Device Access:**
   - Old: `device.capacity`, `device.available`
   - New: `device['capacity']`, `device['available']`

### Upgrade Path:
```python
# Update code using ResourceGraphManager
from jarvis_cd.util.resource_graph import ResourceGraphManager

# Old code:
mgr = ResourceGraphManager()
mgr.load_resource_graph()
mgr.show_resource_graph()

# New code:
mgr = ResourceGraphManager()  # Auto-loads now!
mgr.show()  # Simplified method name
```

---

## Statistics

- **Total Commits:** 2
- **Files Changed:** 20 unique files
- **Lines Added:** 790+
- **Lines Removed:** 264
- **Net Growth:** +526 lines
- **Documentation Added:** ~200 lines
- **New Features:** 3 CLI commands
- **Bug Fixes:** 1 critical fix (capacity tracking)
- **Refactorings:** 2 major (ResourceGraph, Pipeline)

---

## Next Steps

1. **Merge the recovery branch:**
   ```bash
   git checkout 36-refactor-with-ai
   git merge recovery-phase-14
   ```

2. **Run tests:**
   ```bash
   pytest tests/
   ```

3. **Verify documentation:**
   - Check all doc links work
   - Verify code examples are accurate
   - Test commands in documentation

4. **Update any dependent code:**
   - Search for old ResourceGraphManager method calls
   - Update StorageDevice class references
   - Fix any broken imports

5. **Create PR if needed:**
   ```bash
   git push origin recovery-phase-14
   # Create PR: recovery-phase-14 → 36-refactor-with-ai
   ```

---

## Files Modified Summary

### Core System Files
- `jarvis_cd/core/cli.py` - Major CLI enhancements
- `jarvis_cd/core/config.py` - Configuration improvements
- `jarvis_cd/core/module_manager.py` - Module management features
- `jarvis_cd/core/pipeline.py` - Pipeline refactoring
- `jarvis_cd/core/pkg.py` - Package management updates
- `jarvis_cd/core/resource_graph.py` - Resource graph integration
- `jarvis_cd/util/resource_graph.py` - Major refactoring
- `jarvis_cd/util/__init__.py` - Utility improvements
- `jarvis_cd/shell/process.py` - Process handling enhancements

### Binary Files
- `bin/jarvis_resource_graph` - Critical bug fix
- `bin/jarvis-install-builtin` - Removed (obsolete)

### Documentation Files
- `docs/modules.md` - Module management guide
- `docs/package_dev_guide.md` - Package development guide
- `docs/pipelines.md` - Pipeline documentation
- `docs/resource_graph.md` - Resource graph guide
- `.claude/agents/git-expert.md` - New agent config

### Configuration Files
- `pyproject.toml` - Project configuration
- `setup.py` - Setup simplification
- `MANIFEST.in` - Manifest updates

### AI Prompt Files
- `ai-prompts/phase3-launch.md` - Phase 3 updates
- `ai-prompts/phase5-jarvis-repos.md` - Phase 5 updates

---

## Command Reference - What Was Added

### New CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `jarvis mod clear <module>` | Clear module directory (keep src/) | `jarvis mod clear mymod` |
| `jarvis mod dep add <mod> <dep>` | Add dependency to module | `jarvis mod dep add mymod hermes` |
| `jarvis mod dep remove <mod> <dep>` | Remove dependency from module | `jarvis mod dep remove mymod hermes` |

### Modified Commands (Simplified)

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `ResourceGraphManager.build_resource_graph()` | `.build()` | Shorter, cleaner |
| `ResourceGraphManager.load_resource_graph()` | `.load()` | Auto-loads on init now |
| `ResourceGraphManager.show_resource_graph()` | `.show()` | Shows raw YAML |
| `ResourceGraphManager.show_resource_graph_path()` | `.show_path()` | Simpler name |

---

## Lessons Learned

1. **Always create branches before making changes** - Even in detached HEAD state
2. **Git reflog is your friend** - Saved all this work!
3. **Document as you go** - This recovery would have been harder without commit messages
4. **Regular commits** - Two well-structured commits made recovery straightforward
```
