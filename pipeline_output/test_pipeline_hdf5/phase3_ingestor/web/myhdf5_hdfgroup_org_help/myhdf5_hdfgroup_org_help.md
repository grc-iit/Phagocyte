# myHDF5
[Open HDF5](https://myhdf5.hdfgroup.org/ "Open HDF5")[Help](https://myhdf5.hdfgroup.org/help "Help")
## Opened files
To get started, please open a file
Made by [PaNOSC](https://www.panosc.eu/) at [ESRF](https://www.esrf.fr/)
## About myHDF5
_myHDF5_ is an online **HDF5 file viewing service** developed and maintained by the [European Synchrotron Radiation Facility](https://www.esrf.fr/) (ESRF) as part of the European [PaNOSC project](https://www.panosc.eu/). It is based on [**H5Web**](https://github.com/silx-kit/h5web), a React/WebGL viewer for exploring and visualising HDF5 files, as well as [**h5wasm**](https://github.com/usnistgov/h5wasm), a WebAssembly port of the HDF5 C library developed by the [NIST](https://www.nist.gov/) that allows reading HDF5 files with JavaScript.
## Opening local files
myHDF5 supports opening local HDF5 files of **any size** , either by selecting them via a file picker from the [_Open HDF5_](https://myhdf5.hdfgroup.org/) page, or by dragging and dropping them anywhere on the interface at any time. You can even select/drop multiple files at once. Note that your files are **never uploaded** to a remote server; everything happens locally in your browser thanks to [h5wasm](https://github.com/usnistgov/h5wasm).
## Opening remote files
myHDF5 supports opening HDF5 files that are served statically through the web. To do so, simply paste the URL of a file in the field located on the [_Open HDF5_](https://myhdf5.hdfgroup.org/) page. Note that the server must accept [cross-origin requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).
A number of hosting services such as Zenodo and GitHub allow downloading raw files. However, it is not always easy to find the right URL to use. To make it easier, myHDF5 accepts the following user-facing URL formats:
  * **Zenodo** download URL (from a [record page](https://zenodo.org/record/6497438), right-click on file, _Copy Link_)
e.g. [https://zenodo.org/record/6497438/files/xrr_dataset.h5?download=1](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fzenodo.org%2Frecord%2F6497438%2Ffiles%2Fxrr_dataset.h5%3Fdownload%3D1)
  * **GitHub[permalink](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files)** (recommended for sharing)
e.g. [https://github.com/oasys-esrf-kit/dabam2d/blob/f3aed913976d5772a51e6bac3bf3c4e4e4c8b4e1/data/dabam2d-0001.h5](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2Foasys-esrf-kit%2Fdabam2d%2Fblob%2Ff3aed913976d5772a51e6bac3bf3c4e4e4c8b4e1%2Fdata%2Fdabam2d-0001.h5 "https://github.com/oasys-esrf-kit/dabam2d/blob/f3aed913976d5772a51e6bac3bf3c4e4e4c8b4e1/data/dabam2d-0001.h5")
  * GitHub URL with tag, branch or commit sha
e.g. [https://github.com/oasys-esrf-kit/dabam2d/blob/main/data/dabam2d-0001.h5](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2Foasys-esrf-kit%2Fdabam2d%2Fblob%2Fmain%2Fdata%2Fdabam2d-0001.h5)
e.g. [https://github.com/oasys-esrf-kit/dabam2d/blob/f3aed913976d5772a51e6bac3bf3c4e4e4c8b4e1/data/dabam2d-0001.h5](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2Foasys-esrf-kit%2Fdabam2d%2Fblob%2Ff3aed913976d5772a51e6bac3bf3c4e4e4c8b4e1%2Fdata%2Fdabam2d-0001.h5 "https://github.com/oasys-esrf-kit/dabam2d/blob/f3aed913976d5772a51e6bac3bf3c4e4e4c8b4e1/data/dabam2d-0001.h5")


Note that **GitLab** currently [does not support](https://gitlab.com/gitlab-org/gitlab/-/issues/16732) cross-origin requests. You can still paste a user-facing GitLab URL, but myHDF5 won't be able to fetch the file and will show an error. When this occurs, myHDF5 lets you download the file manually so you can open it as a local file.e.g. [https://gitlab.com/utopia-project/utopia/-/blob/master/test/core/cell_manager_test.h5](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgitlab.com%2Futopia-project%2Futopia%2F-%2Fblob%2Fmaster%2Ftest%2Fcore%2Fcell_manager_test.h5)
## Sharing a link to myHDF5
When opening a remote file (i.e. a file hosted on Zenodo, GitHub, etc.), the URL of myHDF5 shown in the browser's address bar is **shareable as is**. _This feature does not work for local files._
## Supported HDF5 compression plugins
myHDF5 supports reading datasets compressed with any of the plugins available in [h5wasm‑plugins@0.0.3](https://github.com/h5wasm/h5wasm-plugins/tree/v0.0.3?tab=readme-ov-file#included-plugins).
## Known limitations
  * External links and virtual datasets in HDF5 files are not supported. While you should see an explicit error for external links, it won't be the case for virtual datasets, which will appear filled with zeros (or with the dataset's [fill value](https://docs.hdfgroup.org/hdf5/develop/group___d_c_p_l.html#title28), if set).
  * Local files are not persisted. If you leave myHDF5 and come back later, or even just reload the page, local files will be removed from the list of opened files.


## Where to find support
  * For issues/features related to the H5Web viewer, please use [H5Web's issue tracker](https://github.com/silx-kit/h5web/issues) on GitHub
  * Otherwise, please use [myHDF5's issue tracker](https://github.com/silx-kit/myhdf5/issues) on GitLab
  * You can also contact us on H5Web's support & feedback mailing list: h5web@esrf.fr


## Where to leave feedback
We'd love to hear what you think of myHDF5 and the H5Web viewer! Here are the best ways to get in touch with us:
  * [Open a discussion thread](https://github.com/silx-kit/h5web/discussions) on H5Web's GitHub repository
  * Drop us a line at h5web@esrf.fr


