# Jarvis-CD: HPC Deployment System - Architecture, Configuration, Deployment Pipelines, and Storage Integration

**Key Points**
*   **Unified Deployment Platform:** Jarvis-CD is a Python-based infrastructure designed to automate the deployment of complex software stacks, particularly storage systems and benchmarks, on heterogeneous High-Performance Computing (HPC) clusters.
*   **Resource Graph Abstraction:** A core architectural component is the "Resource Graph," a machine-readable snapshot of a cluster's hardware (storage, network, accelerators) that allows deployment pipelines to be portable and hardware-aware.
*   **Pipeline-Based Workflow:** Deployments are organized into "pipelines," which are ordered sets of configured "packages" (services, applications, or interceptors) that execute in a defined sequence.
*   **Storage Specialization:** The system is deeply integrated with hierarchical storage systems like Hermes and OrangeFS, automating the generation of complex configuration files and the injection of I/O interceptors.

---

## 1. Introduction

Modern High-Performance Computing (HPC) environments are becoming increasingly heterogeneous, incorporating diverse storage technologies (NVMe, PMEM), accelerators (GPUs, TPUs), and interconnects. This diversity presents a significant challenge for researchers and system administrators who must deploy complex software stacks that are optimized for specific hardware configurations [1]. **Jarvis-CD** (Continuous Delivery) addresses this challenge by providing a unified, extensible framework for defining, deploying, and managing HPC applications and storage systems.

Developed primarily by the Gnosis Research Center at the Illinois Institute of Technology, Jarvis-CD serves as a "Platform Plugins Interface" [2]. It abstracts the complexity of manual configuration scripts and "dependency hell" by encapsulating software into reusable **Packages** and orchestrating them through **Pipelines**. A distinguishing feature of Jarvis-CD is its focus on reproducibility and portability; it utilizes a **Resource Graph** to map software requirements to available hardware dynamically, allowing the same pipeline to run optimally across different clusters without manual reconfiguration [3].

This report details the architecture of Jarvis-CD, its configuration mechanisms, the structure of its deployment pipelines, and its specific capabilities regarding storage system integration.

---

## 2. System Architecture

The architecture of Jarvis-CD is built around the concept of modularity and hardware abstraction. It is implemented as an extensible Python framework that interacts with the underlying system through a set of utilities and abstractions [1].

### 2.1 Core Components

The system is composed of three primary architectural layers: the **Package (Pkg)** layer, the **Pipeline** orchestration layer, and the **Resource Graph** abstraction layer.

#### 2.1.1 Packages (Pkgs)
In Jarvis-CD, an application or service is encapsulated as a "package" (or `pkg`). A package is a Python class that inherits from a base `Pkg` class, defining how the software should be configured, started, stopped, and monitored [4]. Jarvis-CD categorizes packages into three distinct types to handle different lifecycle requirements [3, 5]:

1.  **Service:** A long-running program that executes indefinitely until forcibly stopped. Examples include storage daemons like OrangeFS servers or the Hermes daemon.
2.  **Application:** A program that runs to a definite completion. This category typically includes benchmarks (e.g., IOR, FIO) or scientific simulations (e.g., Gray-Scott, WRF).
3.  **Interceptor:** A library or tool used to intercept function calls, typically for monitoring or redirecting I/O. Examples include the Hermes MPI-IO interceptor or profiling tools like Darshan.

The `Pkg` base class provides standardized methods and attributes, such as `self.config` for package-specific settings and `self.env` for environment variables, ensuring a consistent interface for all software [4].

#### 2.1.2 The Resource Graph
To solve the problem of hardware heterogeneity, Jarvis-CD introduces the **Resource Graph**. This is a YAML-based schema that acts as a snapshot of a cluster's specific hardware configuration, including storage devices, mount points, network interfaces, and memory hierarchy [3, 5].

*   **Function:** It allows packages to query the environment dynamically. For example, a storage package can query the Resource Graph to ask, "Are there local NVMe drives available on the compute nodes?" or "Does the network support Verbs?" [3].
*   **Portability:** By relying on the Resource Graph rather than hardcoded paths, pipelines become portable. A pipeline defined on one machine can be moved to another; Jarvis-CD will regenerate the necessary configurations based on the new machine's Resource Graph [1].
*   **Structure:** The graph typically includes a list of file systems (`fs`), detailing availability, device types (SSD, HDD), mount points, and whether the storage is shared or local [6].

#### 2.1.3 Jarvis-Util
Underpinning the deployment logic is **jarvis-util**, a support library that handles low-level execution details. It provides Python wrappers for common HPC operations, such as executing commands via MPI (Message Passing Interface) or PSSH (Parallel SSH), managing hostfiles, and handling shell command execution [3, 7]. This separation of concerns allows the core Jarvis-CD logic to focus on orchestration while `jarvis-util` handles the mechanics of distributed execution.

### 2.2 Integration with Schedulers
Jarvis-CD is designed to work within the constraints of HPC job schedulers. It integrates with systems like **SLURM** and **PBS**, allowing it to manage job allocations and execute pipelines within reserved compute nodes [1]. This integration ensures that Jarvis-CD can be used for both interactive development and large-scale batch processing.

---

## 3. Configuration and Bootstrapping

Configuring Jarvis-CD involves setting up the environment to recognize the specific machine's layout and defining where metadata and persistent data should be stored.

### 3.1 Bootstrapping
Jarvis-CD supports three primary bootstrapping modes to initialize the environment [7, 8]:

1.  **Single Machine (Local):** Used for testing on a single node (e.g., a laptop or a single server). The command `jarvis bootstrap from local` configures Jarvis to run everything locally.
2.  **Existing Machine:** For known HPC clusters (e.g., machines at IIT, Sandia, or Argonne), Jarvis includes pre-configured profiles. Users can run `jarvis bootstrap from [machine-name]` to automatically load the correct Resource Graph and system defaults.
3.  **New Configuration:** For custom or undefined clusters, users must initialize a new configuration manually using `jarvis init`.

### 3.2 Directory Structure
A proper Jarvis-CD installation relies on three critical directory definitions, which are stored in the main configuration file (`jarvis_config.yaml`) [7]:

*   **`CONFIG_DIR`:** Stores metadata for packages and pipelines. This directory contains the definitions of created pipelines and their specific configurations. It must be accessible by the user (e.g., in the user's home directory).
*   **`PRIVATE_DIR`:** A directory that is common across all machines (same path) but stores data **locally** to each machine. This is crucial for shared-nothing architectures or distributed storage systems like OrangeFS that require local metadata storage on each node.
*   **`SHARED_DIR`:** A directory that is common across all machines and provides a **unified view** of the data (e.g., an NFS or Lustre mount). This is used to store configuration files that must be identical across all nodes (e.g., the Hermes configuration file) [4].

### 3.3 Hostfile Management
Jarvis-CD utilizes a hostfile system similar to MPI to define the set of nodes available for a pipeline.
*   **Format:** The hostfile lists nodes (e.g., `node-01`, `node-[02-05]`) [9].
*   **Active Hostfile:** Users set an active hostfile using `jarvis hostfile set /path/to/hostfile`.
*   **Introspection:** When building the Resource Graph (`jarvis rg build`), Jarvis uses the hostfile to inspect the nodes. It is recommended to have at least two nodes in the hostfile during this step to accurately detect valid networks and interconnects between hosts [7].

---

## 4. Deployment Pipelines

The **Pipeline** is the central operational unit in Jarvis-CD. It represents an end-to-end workflow, chaining together services, interceptors, and applications into a single executable entity.

### 4.1 Pipeline Definition
A pipeline is defined as an ordered set of configured packages. For example, a storage I/O research pipeline might consist of:
1.  **Service:** A storage system (e.g., Hermes or OrangeFS) to manage data.
2.  **Interceptor:** A profiling tool (e.g., the Hermes MPI-IO interceptor) to capture I/O calls.
3.  **Application:** A benchmark (e.g., IOR) to generate load.

This structure allows users to orchestrate complex dependencies, ensuring that the storage service is fully active before the application begins execution [5].

### 4.2 Creating and Managing Pipelines
Jarvis-CD provides a Command Line Interface (CLI) for managing the pipeline lifecycle [4, 10]:

*   **Creation:** `jarvis ppl create [pipeline_name]` initializes a new, empty pipeline.
*   **Appending Packages:** `jarvis ppl append [pkg_name]` adds a package to the pipeline.
*   **Configuration:** `jarvis pkg configure [pkg_name] [parameters]` allows users to modify specific settings for a package within the pipeline (e.g., setting `sleep=5` for a service or `xfer=1m` for a benchmark).
*   **Environment Management:** `jarvis ppl env copy [env_name]` allows pipelines to inherit or snapshot environment variables, ensuring consistent execution contexts.

### 4.3 Execution Flow
When a pipeline is executed, Jarvis-CD processes the packages in the defined order.
1.  **Services** are started first. Jarvis ensures they are running and healthy.
2.  **Environment Variables** (including `LD_PRELOAD` for interceptors) are set automatically based on the pipeline configuration [10].
3.  **Applications** are executed.
4.  **Teardown:** Once the application completes, Jarvis can stop the services, ensuring a clean cleanup of resources.

### 4.4 Reproducibility
Pipelines serve as static records of an experiment. Because the pipeline definition includes the specific versions of packages, their configuration parameters, and the environment state, researchers can share pipeline definitions to reproduce experiments exactly on different hardware (leveraging the Resource Graph for adaptation) [3].

---

## 5. Storage Integration

One of Jarvis-CD's primary motivations is to manage the complexity of modern storage systems. It provides deep integration with several storage solutions, automating the tedious and error-prone process of configuration generation.

### 5.1 Hermes Integration
**Hermes** is a hierarchical buffering system that manages I/O across heterogeneous storage tiers (RAM, NVMe, Burst Buffers). Jarvis-CD is the recommended deployment method for Hermes [10].

*   **Configuration Generation:** Hermes requires a complex configuration file detailing the capacity, mount points, and hierarchy of available storage devices. Jarvis-CD automates this by querying the **Resource Graph**. It identifies valid buffering locations and networks, generating the Hermes configuration file automatically and placing it in the `SHARED_DIR` so all nodes see the same topology [4, 8].
*   **Interceptor Injection:** To use Hermes transparently, applications must preload the Hermes library. Jarvis-CD handles this by appending the `hermes_api` package (configured with `+mpi` for MPI-IO interception) to the pipeline. It automatically sets the `LD_PRELOAD` environment variable for subsequent applications in the pipeline [10].

### 5.2 OrangeFS Integration
**OrangeFS** is a parallel file system that is often used in research.
*   **Per-Machine Data:** OrangeFS requires specific metadata and data storage directories on each server. Jarvis-CD utilizes the `PRIVATE_DIR` configuration to ensure that each node stores its local OrangeFS state in the correct location, distinct from the shared configuration files [7, 10].
*   **Service Management:** Jarvis-CD manages the OrangeFS server processes, handling startup and shutdown sequences across the cluster nodes defined in the hostfile.

### 5.3 Other Systems
The extensible nature of Jarvis-CD allows it to support various other systems.
*   **DAOS & Lustre:** The framework includes packages for managing DAOS (Distributed Asynchronous Object Storage) and Lustre, allowing users to deploy these complex parallel file systems as part of user-space pipelines [1].
*   **MegaMmap:** Research into distributed shared memory systems (like MegaMmap) utilizes Jarvis-CD to manage the deployment of memory-centric storage stacks, leveraging the Resource Graph to configure tiered DRAM and storage management policies [6].

---

## 6. Conclusion

Jarvis-CD represents a significant advancement in the management of HPC software stacks. By decoupling the definition of a software pipeline from the specifics of the hardware it runs on (via the Resource Graph), it enables true portability and reproducibility in I/O research. Its architecture—comprising modular Packages, orchestrated Pipelines, and robust hardware abstractions—simplifies the deployment of complex, multi-component storage systems like Hermes and OrangeFS, allowing researchers to focus on scientific discovery rather than configuration management.

---

## References

### Publications

#### Conference Papers
[11] "Jarvis: Towards a Shared, User-Friendly, and Reproducible, I/O Infrastructure" (Cernuda et al.). PDSW'24: The 9th International Parallel Data Systems Workshop, 2024. | http://cs.iit.edu/~scs/assets/files/cernuda2024jarvis.pdf
[12] "PDSW'24 WIP: Jarvis" (Cernuda et al.). PDSW'24 Work in Progress Session, 2024. | https://pdsw.org/pdsw24/slides/pdsw24_wip_session2_wip1.pdf
[13] "MegaMmap: A High-Performance Distributed Shared Memory for Data-Intensive Applications" (Kougkas et al.). 2024. | https://akougkas.io/assets/pdf/megammap.pdf

### Code & Tools
[14] jarvis-cd - Jarvis-cd is a unified platform for deploying various applications. https://github.com/grc-iit/jarvis-cd
[15] runtime-deployment - Jarvis-cd repository mirror/fork. https://github.com/iowarp/runtime-deployment

### Documentation
[7] "Jarvis-CD Index." Jarvis-CD Documentation. https://grc.iit.edu/docs/jarvis/jarvis-cd/index/
[5] "Design & Motivation." Jarvis-CD Documentation. https://grc.iit.edu/docs/jarvis/jarvis-cd/design-motivation/
[2] "Deploying Hermes." Hermes Documentation. https://grc.iit.edu/docs/hermes/deploying-hermes/
[9] "Jarvis-CD Storage Integration." IOWarp Documentation. https://grc.iit.edu/docs/iowarp/deployment/jarvis/
[16] "Building a Package." Jarvis-CD Documentation. https://grc.iit.edu/docs/jarvis/jarvis-cd/building-package/