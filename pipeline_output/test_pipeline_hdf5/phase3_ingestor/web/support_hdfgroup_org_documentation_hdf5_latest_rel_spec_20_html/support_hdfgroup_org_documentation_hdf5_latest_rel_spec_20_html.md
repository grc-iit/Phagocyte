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
  * [ HDF5 Library and Tools 2.0.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title0 "H1")
  * [ Release Information](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title1 "H2")
  * [ Downloads](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title2 "H2")
  * [ Methods to obtain (gz file)](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title3 "H2")
  * [ Doxygen Generated Reference Manual](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title4 "H2")
  * [ Migrating from HDF5 1.14 to HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title5 "H1")
  * [ New Features in HDF5 Release 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#title6 "H1")


[•All](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))
Loading...
Searching...
No Matches
Release Specific Information for HDF5 2.0
Navigate back: [Main](https://support.hdfgroup.org/documentation/hdf5/latest/index.html) / [Release Specific Information](https://support.hdfgroup.org/documentation/hdf5/latest/release_specific_info.html)
* * *
#  HDF5 Library and Tools 2.0.0
##  Release Information
Version  | HDF5 2.0.0   
---|---  
Release Date  | 11/10/25   
Additional Release Information  |  [Change log](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/CHANGELOG.md)  
|  [Migrating from HDF5 1.14 to HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#sec_rel_spec_20_migrate)  
|  [Software Changes from Release to Release in HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#sec_rel_spec_20_change)  
|  [New Features in HDF5 Release 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html#sec_rel_spec_20_feat)  
|  [Newsletter Announcement](https://www.hdfgroup.org/2025/11/10/release-of-hdf5-2-0-0-newsletter-207/)  
| ABI/API Compatibility Reports between 2.0.0 and 1.14.6 [tar file](https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.html.abi.reports.tar.gz) or [individual html files](https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/compat_report/index.html)  
|  [Doxygen generated Reference Manual](https://support.hdfgroup.org/documentation/hdf5/latest/)  
##  Downloads
Source code and binaries are available at: [HDF5 2.0.0 on GitHub](https://github.com/HDFGroup/hdf5/releases/tag/2.0.0)
Please refer to [Build instructions](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/INSTALL) for building with CMake.
##  Methods to obtain (gz file)
  * firefox – Download file and then run: `gzip <distribution>.tar.gz | tar xzf -`
  * chrome – Download file and then run: `gzip -cd <distribution>.tar.gz | tar xvf -`
  * wget – 
`wget https://github.com/HDFGroup/hdf5/releases/download/[](https://github.com/HDFGroup/hdf5/releases/download/)${PACKAGEVERSION}/<distribution>.tar.gz`  
`gzip -cd <distribution>.tar.gz | tar xvf -`
  * `<distribution>` is hdf5-${PACKAGEVERSION}, where PACKAGEVERSION is 2.0.0 for this release


##  Doxygen Generated Reference Manual
The new HDF5 documentation based on [Doxygen](https://www.doxygen.nl/index.html) is available [here](https://support.hdfgroup.org/documentation/hdf5/latest/index.html).
This documentation is WORK-IN-PROGRESS.
Since this portion of the HDF5 documentation is now part of the source code, it gets the same treatment as code. In other words, issues, inaccuracies, corrections should be reported as issues in [GitHub](https://github.com/HDFGroup/hdf5/issues), and pull requests will be reviewed and accepted as any other code changes.
#  Migrating from HDF5 1.14 to HDF5 2.0
This section highlights some changes that might affect migrating to HDF5.20, please refer to the [Software Changes from Release to Release in HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#sec_rel_spec_20_change) or the [Change log](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/CHANGELOG.md) for detail.
  * Default file format is now 1.8 
  * The file format has been updated to 4.0
  * API signature changes
    * `H5Dread_chunk()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#a8ff3b0cf52e30e2e12d617aa2329486e)`  

    * `H5Tdecode()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#ac90f7722dacad861c0a22507d3adf0dd)`  

    * `H5Iregister_type()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#af51df104e1e3ff0b99b7a8ca368f14ab)`  

  * A new backend based on the [aws-c-s3 library](https://github.com/awslabs/aws-c-s3) replaced the ROS3 VFD's S3 backend based on libcurl. The ROS3 VFD now requires the `aws-c-s3` library in order to be built. See the [Change log](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/CHANGELOG.md) for a complete description on this feature. 
  * Significance in tools
    * The tool h5dump has a new option `--lformat` and its `XML` option is deprecated.
    * The high-level GIF tools, `h52gif` and `gif2h5` have been removed. We may move them to a separate repository in the future. See [Change log](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/CHANGELOG.md) for an explanation.


#  New Features in HDF5 Release 2.0
This section includes the new features introduced in the HDF5 2.0 series:
  * [Support for Complex number datatypes](https://support.hdfgroup.org/releases/hdf5/documentation/rfc/RFC__Adding_support_for_16_bit_floating_point_and_Complex_number_datatypes_to_HDF5.pdf)   
Support for the C99 `float _Complex`, `double _Complex` and `long double _Complex` (with MSVC, `_Fcomplex`, `_Dcomplex` and `_Lcomplex`) types has been added for platforms/compilers that support them. These types have been implemented with a new datatype class, `H5T_COMPLEX`. Note that any datatypes of class H5T_COMPLEX will not be readable with previous versions of HDF5. If a file is accessed with a library version bounds "high" setting less than `H5F_LIBVER_V200`, an error will occur if the application tries to create an object with a complex number datatype. If compatibility with previous versions of HDF5 is desired, applications should instead consider adopting [one of the existing conventions](https://nc-complex.readthedocs.io/en/latest/#conventions-used-in-applications).  



  * An AWS endpoint command option   
The new option is `--endpoint-url`, which allows the user to set an alternate endpoint URL other than the standard "protocol://service-code.region-code.amazonaws.com". If `--endpoint-url` is not specified, the ROS3 VFD will first check the `AWS_ENDPOINT_URL_S3` and `AWS_ENDPOINT_URL` environment variables for an alternate endpoint URL before using a default one, with the region-code being supplied by the FAPL or standard AWS locations/environment variables.   
This option is supported by the following tools: `h5dump`, `h5ls`, `h5stat`


  * Specifying ROS3 VFD on the command line is not required when using S3 URI   
This feature applies to the following tools: `h5dump`, `h5ls`, `h5stat`.


  * Performance improvement in opening a virtual dataset with many mappings   
When opening a virtual dataset, the library would previously decode the mappings in the object header package, then copy them to the dataset struct, then copy them to the internal dataset creation property list. Copying the VDS mappings could be very expensive if there were many mappings. Changed this to delay decoding the mappings until the dataset code, and delay copying the layout to the DCPL until it is needed. This results in only the decoding and no copies in most use cases, as opposed to the decoding and two copies with the previous code.


  * Support for chunks larger than 4 GiB using 64 bit addressing.


  * New predefined datatypes for
    * FP8 data in E4M3 and E5M2 formats (<https://arxiv.org/abs/2209.05433>), but not a native FP8 datatype.
    * little- and big-endian [bfloat16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) data.   
Please refer to the [CHANGELOG](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/CHANGELOG.md) for detail.


  * Default chunk cache hash table size increased to 8191   
In order to reduce hash collisions and take advantage of modern memory capacity, the default hash table size for the chunk cache has been increased from 521 to 8191. This means the hash table will consume approximately 64 KiB per open dataset. This value can be changed with `H5Pset_cache()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___f_a_p_l.html#ga034a5fc54d9b05296555544d8dd9fe89 "Sets the raw data chunk cache parameters.")` or `H5Pset_chunk_cache()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___d_a_p_l.html#ga104d00442c31714ee073dee518f661f1 "Sets the raw data chunk cache parameters.")`. This value was chosen because it is a prime number close to 8K.


[Software Changes from Release to Release in HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#sec_rel_spec_20_change)
* * *
Navigate back: [Main](https://support.hdfgroup.org/documentation/hdf5/latest/index.html) / [Release Specific Information](https://support.hdfgroup.org/documentation/hdf5/latest/release_specific_info.html)
  * Generated by [![doxygen](https://support.hdfgroup.org/documentation/hdf5/latest/doxygen.svg)](https://www.doxygen.org/index.html) 1.13.2 


