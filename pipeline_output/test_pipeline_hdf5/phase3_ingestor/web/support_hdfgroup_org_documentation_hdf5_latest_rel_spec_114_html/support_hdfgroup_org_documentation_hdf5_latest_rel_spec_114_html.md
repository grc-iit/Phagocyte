Help us improve by taking our short survey: <https://www.hdfgroup.org/website-survey/>
![Logo](https://support.hdfgroup.org/documentation/hdf5/latest/HDFG-logo.png) |  HDF5 Last Updated on 2026-01-01 The HDF5 Field Guide  
---|---  
  * [Main Page](https://support.hdfgroup.org/documentation/hdf5/latest/index.html)
  * [Getting started](https://support.hdfgroup.org/documentation/hdf5/latest/_getting_started.html)
  * [User Guide](https://support.hdfgroup.org/documentation/hdf5/latest/_u_g.html)
  * [Reference Manual](https://support.hdfgroup.org/documentation/hdf5/latest/_r_m.html)
  * [Cookbook](https://support.hdfgroup.org/documentation/hdf5/latest/_cookbook.html)
  * [Technical Notes](https://support.hdfgroup.org/documentation/hdf5/latest/_t_n.html)
  * [RFCs](https://support.hdfgroup.org/documentation/hdf5/latest/_r_f_c.html)
  * [Specifications](https://support.hdfgroup.org/documentation/hdf5/latest/_s_p_e_c.html)
  * [Glossary](https://support.hdfgroup.org/documentation/hdf5/latest/_g_l_s.html)
  * [Full-Text Search](https://support.hdfgroup.org/documentation/hdf5/latest/_f_t_s.html)
  * [About](https://support.hdfgroup.org/documentation/hdf5/latest/_about.html)
  * [![](https://support.hdfgroup.org/documentation/hdf5/latest/search/close.svg)](javascript:searchBox.CloseResultsWindow\(\))


### Table of contents
  * [ HDF5 Library and Tools 1.14.6](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title0 "H1")
  * [ Release Information](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title1 "H2")
  * [ Downloads](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title2 "H2")
  * [ Methods to obtain (gz file)](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title3 "H2")
  * [ Doxygen Generated Reference Manual](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title4 "H2")
  * [ Migrating from HDF5 1.12 to HDF5 1.14](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title5 "H1")
  * [ Migrating to HDF5 1.14 from Previous Versions of HDF5](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title6 "H1")
  * [ API Changes](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title7 "H2")
  * [ H5Iregister_type / H5I_free_t](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title8 "H2")
  * [ Virtual File Layer (VFL) Changes](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title9 "H2")
  * [ Virtual Object Layer (VOL) Changes](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title10 "H2")
  * [ New Features in HDF5 Release 1.14](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#title11 "H1")


[•All](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))
Loading...
Searching...
No Matches
Release Specific Information for HDF5 1.14
Navigate back: [Main](https://support.hdfgroup.org/documentation/hdf5/latest/index.html) / [Release Specific Information](https://support.hdfgroup.org/documentation/hdf5/latest/release_specific_info.html)
* * *
#  HDF5 Library and Tools 1.14.6
##  Release Information
Version  | HDF5 1.14.6   
---|---  
Release Date  | 02/05/25   
Additional Release Information  |  [RELEASE.txt](https://github.com/HDFGroup/hdf5/blob/hdf5_1.14.6/release_docs/RELEASE.txt)  
|  [Migrating from HDF5 1.12 to HDF5 1.14](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#sec_rel_spec_114_migrate)  
|  [Software Changes from Release to Release in HDF5 1.14](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114_change.html#sec_rel_spec_114_change)  
|  [New Features in HDF5 Release 1.14](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114.html#sec_rel_spec_114_feat)  
|  [Newsletter Announcement](https://www.hdfgroup.org/2025/02/05/release-of-hdf5-1-14-6-newsletter-205/)  
| ABI/API compatibility reports between 1.14.6 and 1.14.5 [tar file](https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_6/downloads/hdf5-1.14.6.html.abi.reports.tar.gz) or [individual html files](https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_6/downloads/compat_report/index.html)  
|  [Doxygen generated Reference Manual](https://support.hdfgroup.org/documentation/hdf5/latest/)  
##  Downloads
Source code and binaries are available at: [https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_6](https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_6/downloads/index.html)
Please refer to [Build instructions](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/INSTALL) for building with either CMake or Autotools.
##  Methods to obtain (gz file)
  * firefox – Download file and then run: `gzip <distribution>.tar.gz | tar xzf -`
  * chrome – Download file and then run: `gzip -cd <distribution>.tar.gz | tar xvf -`
  * wget – 
`wget https://github.com/HDFGroup/hdf5/releases/download/[](https://github.com/HDFGroup/hdf5/releases/download/)${PACKAGEVERSION}/<distribution>.tar.gz`  
`gzip -cd <distribution>.tar.gz | tar xvf -`
  * `<distribution>` is hdf5-${PACKAGEVERSION}, where PACKAGEVERSION is 1.14.6 for this release


##  Doxygen Generated Reference Manual
The new HDF5 documentation based on [Doxygen](https://www.doxygen.nl/index.html) is available [here](https://support.hdfgroup.org/documentation/hdf5/latest/index.html).
This documentation is WORK-IN-PROGRESS. Since this portion of the HDF5 documentation is now part of the source code, it gets the same treatment as code. In other words, issues, inaccuracies, corrections should be reported as issues in [GitHub](https://github.com/HDFGroup/hdf5/issues), and pull requests will be reviewed and accepted as any other code changes.
#  Migrating from HDF5 1.12 to HDF5 1.14
#  Migrating to HDF5 1.14 from Previous Versions of HDF5
##  API Changes
There are new API calls that require API Compatibility Macros in HDF5 1.14.0. There are, however, two API calls which have had their signature change.
##  H5Iregister_type / H5I_free_t
The signature of [H5Iregister_type](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#af51df104e1e3ff0b99b7a8ca368f14ab) did not change, but the [H5I_free_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a5f6d1576913865b92856474bfedbe2b4) callback it accepts did have its signature change to add an asynchronous request parameter. There is no API compatibility macro to paper over this change. The request parameter can be ignored in the callback if you are not concerned with asynchronous operations and future IDs. A description of how the request parameter should be used will be found in the (soon to be released) HDF5 Asynchronous Programming Guide. 
  * **Old:** - `typedef herr_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) (*H5I_free_t)(void *obj);`
  * **New:** - `typedef herr_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) (*H5I_free_t)(void *obj, void **request);`


###  H5VLquery_optional
The way optional operations are handled in the virtual object layer (VOL) changed significantly in HDF5 1.14.0. To better support this, the [H5VLquery_optional](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_v_l.html#ga17ef00e528d99eda5879d749c2a12043 "Determine if a VOL connector supports a particular optional callback operation.") API call now takes an output flags parameter instead of a Boolean. Since the entire 1.12 VOL API has been deprecated, no API compatibility macro exists for this API call. 
  * **Old:** - `herr_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) H5VLquery_optional(hid_t obj_id, H5VL_subclass_t subcls, int opt_type, hbool_t *supported);`
  * **New:** - `herr_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) H5VLquery_optional(hid_t obj_id, H5VL_subclass_t subcls, int opt_type, uint64_t *flags)[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_v_l.html#ga17ef00e528d99eda5879d749c2a12043 "Determine if a VOL connector supports a particular optional callback operation.");`


##  Virtual File Layer (VFL) Changes
The virtual file layer has changed in HDF5 1.14.0. Existing virtual file drivers (VFDs) will have to be updated to work with this version of the library.
##  Virtual Object Layer (VOL) Changes
The virtual object layer has changed significantly in HDF5 1.14.0 and the 1.12 VOL API is now considered deprecated and unsupported. Existing virtual object layer connectors should be updated to work with this version of the library.
#  New Features in HDF5 Release 1.14
The new features in the HDF5 1.14 series include: 
  * [Adding support for 16-bit floating point and Complex number datatypes to HDF](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/RFC__Adding_support_for_16_bit_floating_point_and_Complex_number_datatypes_to_HDF5.pdf)  
Support for the 16-bit floating-point _Float16 C type has been added to HDF5. On platforms where this type is available, this can enable more efficient storage of floating-point data when an application doesn't need the precision of larger floating-point datatypes. It can also allow for improved performance when converting between 16-bit floating-point data and data of another HDF5 datatype.


  * [The HDF5 Event Set Interface](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_e_s__u_g.html#sec_async)  
HDF5 provides asynchronous APIs for the HDF5 VOL connectors that support asynchronous HDF5 operations using the HDF5 Event Set (H5ES) API. This allows I/O to proceed in the background while the application is performing other tasks.


  * [VFD Sub-filing](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/RFC_VFD_subfiling_200424.pdf)  
The basic idea behind sub-filing is to find the middle ground between single shared file and one file per process - thereby avoiding some of the complexity of one file per process, and minimizing the locking issues of a single shared file on a parallel file system.


  * [Onion VFD](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/Onion_VFD_RFC_211122.pdf)  
There is a desire to introduce and track modifications to an HDF5 file while preserving or having access to the file as it existed prior to a particular set of modifications. To this end, this RFC proposes an Onion Virtual File Driver (VFD) as an effectively in-file revision management facility. Users will be able to open a particular revision of the file, read from and make modifications to the file, and write to file as a new revision. The name "Onion" derives from a mnemonic: the original file exists with data layered atop one another from an original file to the most recent revision


  * [New HDF5 API Routines for HPC Applications - Read/Write Multiple Datasets in an HDF5 file](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/H5HPC_MultiDset_RW_IO_RFC.pdf)  
The HDF5 library allows a data access operation to access one dataset at a time, whether access is collective or independent. However, accessing multiple datasets will require the user to issue an I/O call for each dataset. This release provides a set of new routines that allow users to access multiple datasets with a single I/O call.


  * New tools h5dwalk and h5delete  
The new tool h5dwalk provides parallelism for improved performance while also including critical logging capabilities to capture outputs from applying the serial tools over large collections of HDF5 files.


Note that the HDF5 Release 1.14.0 is the final released version of all the features that were released in 1.13.0-1.13.3.
#### RFCs
  * [Adding support for 16-bit floating point and Complex number datatypes to HDF](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/RFC__Adding_support_for_16_bit_floating_point_and_Complex_number_datatypes_to_HDF5.pdf)
  * [The HDF5 Event Set Interface](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_e_s__u_g.html#sec_async)
  * [VFD Sub-filing](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/RFC_VFD_subfiling_200424.pdf)
  * [Onion VFD](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/Onion_VFD_RFC_211122.pdf)
  * [New HDF5 API Routines for HPC Applications - Read/Write Multiple Datasets in an HDF5 file](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/H5HPC_MultiDset_RW_IO_RFC.pdf)


[Software Changes from Release to Release in HDF5 1.14](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_114_change.html#sec_rel_spec_114_change)
* * *
Navigate back: [Main](https://support.hdfgroup.org/documentation/hdf5/latest/index.html) / [Release Specific Information](https://support.hdfgroup.org/documentation/hdf5/latest/release_specific_info.html)
  * Generated by [![doxygen](https://support.hdfgroup.org/documentation/hdf5/latest/doxygen.svg)](https://www.doxygen.org/index.html) 1.13.2 


