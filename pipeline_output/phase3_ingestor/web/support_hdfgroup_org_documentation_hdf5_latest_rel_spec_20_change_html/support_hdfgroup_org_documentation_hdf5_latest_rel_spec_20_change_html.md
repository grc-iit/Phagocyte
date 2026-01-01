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
  * [ Software Changes from Release to Release in HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#title0 "H1")
  * [ API Compatibility](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#title1 "H2")
  * [ Differences between releases](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#title2 "H2")


[•All](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))[](javascript:void\(0\))
Loading...
Searching...
No Matches
Release Specific Information for HDF5 2.0
Navigate back: [Main](https://support.hdfgroup.org/documentation/hdf5/latest/index.html) / [Release Specific Information](https://support.hdfgroup.org/documentation/hdf5/latest/release_specific_info.html) / [Release Specific Information for HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html)
* * *
#  Software Changes from Release to Release in HDF5 2.0
This page provides information on the changes that a maintenance developer needs to be aware of between successive releases of HDF5, such as: 
  * New or changed features or tools 
  * Syntax and behavioral changes in the existing application programming interface (the API) 
  * Certain types of changes in configuration or build processes 
  * Note that bug fixes and performance enhancements in the C library are automatically picked up by the C++, Fortran, and Java libraries.


##  API Compatibility
See [API Compatibility Macros](https://support.hdfgroup.org/documentation/hdf5/latest/api-compat-macros.html) for details on using HDF5 version 2.0 with previous releases. 
  * [Compatibility reports for Release 2.0 versus Release 1.14.6](https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.html.abi.reports.tar.gz)


##  Differences between releases
  * [Release 2.0 versus Release 1.14.6](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20_change.html#subsubsec_rel_spec_20_change_0versus14_6)


The [Change log](https://github.com/HDFGroup/hdf5/blob/develop/release_docs/CHANGELOG.md) (a.k.a. the RELEASE.txt prior to release 2.0) also lists changes made to the library, but these notes tend to be more at a more detail-oriented level. It include new features, bugs fixed, supported configuration features, platforms on which the library has been tested, and known problems. The change log files are listed in each release section and can be found at the top level of the HDF5 source code tree in the release_docs directory.
###  Release 2.0 versus Release 1.14.6
HDF5 version 2.0 provides a number of new C APIs and other user-visible changes in behavior in the transition from HDF5 Release 1.14.6 to Release 2.0. Some of those require the use of the API Compatibility Macros for the main library. In addition, some APIs have been removed or have had their signature change.
  * `#hbool_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#ad470b00eccd2115c707c02de5fa1120d)` has been removed from public API calls   
The `#hbool_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#ad470b00eccd2115c707c02de5fa1120d)` type was introduced before the library supported C99's Boolean type. Originally typedef'd to an integer, it has been typedef'd to C99's bool for many years. Prior to HDF5 2.0, it had been purged from the library code and only remained in public API signatures. In HDF5 2.0, it has also been removed from public API signatures.   
The `#hbool_t[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#ad470b00eccd2115c707c02de5fa1120d)` typedef remains in [H5public.h](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html) so existing code does not need to be updated.


  * Default page buffer size for the ROS3 driver changed   
Calling `H5Pset_fapl_ros3()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___f_a_p_l.html#ga9dd7950acea860b716831488dd87ae8f "Modifies the specified File Access Property List to use the H5FD_ROS3 driver.")` now has the side effect of setting the page buffer size in the FAPL to 64 MiB if it was not previously set. This will only have an effect if the file uses paged allocation. Also added the `#H5F_PAGE_BUFFER_SIZE_DEFAULT` to allow the user to unset the page buffer size in an FAPL so it can be similarly overridden.


  * Default dataset chunk cache size increased   
The default dataset chunk cache size was increased to 8 MiB (8,388,608 bytes).


  * [H5Dread_chunk()](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#a8ff3b0cf52e30e2e12d617aa2329486e) signature has changed   
A new parameter, `nalloc`, has been added to `H5Dread_chunk()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#a8ff3b0cf52e30e2e12d617aa2329486e)`. This parameter contains a pointer to a variable that holds the size of the buffer buf. If *nalloc is not large enough to hold the entire chunk being read, no data is read. On exit, the value of this variable is set to the buffer size needed to read the chunk. The old signature has been renamed to `H5Dread_chunk1()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#gad3b9b3024ca4ab7eb7fe6872088398f3 "Reads a raw data chunk directly from a dataset in a file into a buffer.")` and is considered deprecated: 
[herr_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) [H5Dread_chunk1](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#gad3b9b3024ca4ab7eb7fe6872088398f3)([hid_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a0045db7ff9c22ad35db6ae91662e1943) dset_id, [hid_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a0045db7ff9c22ad35db6ae91662e1943) dxpl_id, const [hsize_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a7f81cce70fb546af88da24d9285d3c1c) *offset, uint32_t *filters, void *buf);
[hid_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a0045db7ff9c22ad35db6ae91662e1943)
int64_t hid_t
**Definition** H5Ipublic.h:60
[herr_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160)
int herr_t
**Definition** H5public.h:252
[hsize_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a7f81cce70fb546af88da24d9285d3c1c)
uint64_t hsize_t
**Definition** H5public.h:304
[H5Dread_chunk1](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#gad3b9b3024ca4ab7eb7fe6872088398f3)
herr_t H5Dread_chunk1(hid_t dset_id, hid_t dxpl_id, const hsize_t *offset, uint32_t *filters, void *buf)
Reads a raw data chunk directly from a dataset in a file into a buffer.
The new signature is `H5Dread_chunk2()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#ga217c9d411dfd4c0732213c7cbd98164c "Reads a raw data chunk directly from a dataset in a file into a buffer.")`. All code should be updated to use this version: 
[herr_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) [H5Dread_chunk2](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#ga217c9d411dfd4c0732213c7cbd98164c)([hid_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a0045db7ff9c22ad35db6ae91662e1943) dset_id, [hid_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a0045db7ff9c22ad35db6ae91662e1943) dxpl_id, const [hsize_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a7f81cce70fb546af88da24d9285d3c1c) *offset, uint32_t *filters, void *buf, size_t *nalloc);
[H5Dread_chunk2](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#ga217c9d411dfd4c0732213c7cbd98164c)
herr_t H5Dread_chunk2(hid_t dset_id, hid_t dxpl_id, const hsize_t *offset, uint32_t *filters, void *buf, size_t *buf_size)
Reads a raw data chunk directly from a dataset in a file into a buffer.
`H5Dread_chunk()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#a8ff3b0cf52e30e2e12d617aa2329486e)` will map to the new signature unless the library is explicitly configured to use an older version of the API.


  * [H5Tdecode()](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#ac90f7722dacad861c0a22507d3adf0dd) signature has changed   
A new parameter, `buf_size`, has been added to `H5Tdecode()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#ac90f7722dacad861c0a22507d3adf0dd)` to prevent walking off the end of the buffer. The old signature has been renamed to `H5Tdecode1()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#gacf3174a0433c2768ca23a1047164c05e "Decodes a binary object description of datatype and returns a new object handle.")` and is considered deprecated: 
[herr_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) [H5Tdecode1](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#gacf3174a0433c2768ca23a1047164c05e)(const void *buf);
[H5Tdecode1](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#gacf3174a0433c2768ca23a1047164c05e)
hid_t H5Tdecode1(const void *buf)
Decodes a binary object description of datatype and returns a new object handle.
The new signature is `H5Tdecode2()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#ga485114ecc0c366fda0d88833dd1083a1 "Decodes a binary object description of datatype and returns a new object handle.")`. All code should be updated to use this version: 
[herr_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5public_8h.html#a3b079ecf932a5c599499cf7e298af160) [H5Tdecode2](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#ga485114ecc0c366fda0d88833dd1083a1)(const void *buf, size_t buf_size);
[H5Tdecode2](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#ga485114ecc0c366fda0d88833dd1083a1)
hid_t H5Tdecode2(const void *buf, size_t buf_size)
Decodes a binary object description of datatype and returns a new object handle.
`H5Tdecode()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#ac90f7722dacad861c0a22507d3adf0dd)` will map to the new signature unless the library is explicitly configured to use an older version of the API.


  * [H5Iregister_type()](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#af51df104e1e3ff0b99b7a8ca368f14ab) signature has changed   
The hash_size parameter has not been used since early versions of HDF5 1.8, so it has been removed and the API call has been versioned. The old signature has been renamed to `H5Iregister_type1()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gab57559f14a16d4375815e45054abad16 "Creates and returns a new ID type.")` and is considered deprecated: 
[H5I_type_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a13afe14178faf81b89fa2167e7ab832b) [H5Iregister_type1](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gab57559f14a16d4375815e45054abad16)(size_t hash_size, unsigned reserved, [H5I_free_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a5f6d1576913865b92856474bfedbe2b4) free_func);
[H5I_type_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a13afe14178faf81b89fa2167e7ab832b)
H5I_type_t
**Definition** H5Ipublic.h:34
[H5I_free_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a5f6d1576913865b92856474bfedbe2b4)
herr_t(* H5I_free_t)(void *obj, void **request)
**Definition** H5Ipublic.h:82
[H5Iregister_type1](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gab57559f14a16d4375815e45054abad16)
H5I_type_t H5Iregister_type1(size_t hash_size, unsigned reserved, H5I_free_t free_func)
Creates and returns a new ID type.
The new signature is [H5Iregister_type2()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gad698dd84ea83ade847ffd6c49bc865e2 "Creates and returns a new ID type."). New code should use this version: 
[H5I_type_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a13afe14178faf81b89fa2167e7ab832b) [H5Iregister_type2](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gad698dd84ea83ade847ffd6c49bc865e2)(unsigned reserved, [H5I_free_t](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_ipublic_8h.html#a5f6d1576913865b92856474bfedbe2b4) free_func);
[H5Iregister_type2](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gad698dd84ea83ade847ffd6c49bc865e2)
H5I_type_t H5Iregister_type2(unsigned reserved, H5I_free_t free_func)
Creates and returns a new ID type.
`H5Iregister_type()[](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#af51df104e1e3ff0b99b7a8ca368f14ab)` will map to the new signature unless the library is explicitly configured to use an older version of the API.


List of new public APIs/Macros
Function/Constant | Description   
---|---  
[H5Dread_chunk1()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#gad3b9b3024ca4ab7eb7fe6872088398f3 "Reads a raw data chunk directly from a dataset in a file into a buffer.") | Reads an entire chunk from the file directly (Deprecated in favor of `H5Dread_chunk2()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#ga217c9d411dfd4c0732213c7cbd98164c "Reads a raw data chunk directly from a dataset in a file into a buffer.")`)   
[H5Dread_chunk2()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html#ga217c9d411dfd4c0732213c7cbd98164c "Reads a raw data chunk directly from a dataset in a file into a buffer.") | Reads an entire chunk from the file directly   
[H5Iregister_type1()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gab57559f14a16d4375815e45054abad16 "Creates and returns a new ID type.") | Creates a new type of ID (Deprecated in favor of `H5Iregister_type2()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gad698dd84ea83ade847ffd6c49bc865e2 "Creates and returns a new ID type.")`)   
[H5Iregister_type2()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_i_u_d.html#gad698dd84ea83ade847ffd6c49bc865e2 "Creates and returns a new ID type.") | Creates a new type of ID   
[H5Pget_virtual_spatial_tree()](https://support.hdfgroup.org/documentation/hdf5/latest/group___d_c_p_l.html#ga39ac9ba6cc5c86c3dd8c46bae0ee17e9 "Retrieves the setting for whether or not to use a spatial tree for VDS mappings.") | Retrieves the setting for whether or not to use a spatial tree for VDS mappings   
[H5Pset_virtual_spatial_tree()](https://support.hdfgroup.org/documentation/hdf5/latest/group___d_c_p_l.html#ga5a83d2c1075cc5ff47460b5526ec23ff "Sets the flag to use a spatial tree for mappings.") | Sets the flag to use a spatial tree for mappings   
[H5Tcomplex_create()](https://support.hdfgroup.org/documentation/hdf5/latest/group___c_o_m_p_l_e_x.html#ga94d0f9813a6a69487ea71b20acafd9d4 "Creates a new complex number datatype.") | Creates a new complex number datatype   
[H5Tdecode1()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#gacf3174a0433c2768ca23a1047164c05e "Decodes a binary object description of datatype and returns a new object handle.") | Decodes a binary object description (Deprecated in favor of `H5Tdecode2()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#ga485114ecc0c366fda0d88833dd1083a1 "Decodes a binary object description of datatype and returns a new object handle.")`)   
[H5Tdecode2()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_t.html#ga485114ecc0c366fda0d88833dd1083a1 "Decodes a binary object description of datatype and returns a new object handle.") | Decodes a binary object description   
[H5VLclose_lib_context()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_v_l_d_e_v.html#gae05f169607f8be714fd34424c3786ee0 "Closes the internal state of the HDF5 library.") | Closes the state of the library, undoing the effects of `H5VLopen_lib_context()[](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_v_l_d_e_v.html#gae3b0dc77bc58f9d84cbeb733da1cb94d "Opens a new internal context for the HDF5 library.")`  
[H5VLopen_lib_context()](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_v_l_d_e_v.html#gae3b0dc77bc58f9d84cbeb733da1cb94d "Opens a new internal context for the HDF5 library.") | Opens a new internal context for the HDF5 library   
[H5T_COMPLEX_IEEE_F16BE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_c_o_m_p_l_e_x.html#gad5759434265beea7545d170a17033410) | Complex number of 2 16-bit big-endian IEEE floating point numbers   
[H5T_COMPLEX_IEEE_F16LE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_c_o_m_p_l_e_x.html#ga3a5ac018d52f68b0453a9dbfbd3cb259) | Complex number of 2 16-bit little-endian IEEE floating point numbers   
[H5T_COMPLEX_IEEE_F32BE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_c_o_m_p_l_e_x.html#ga2e539a7d52c9f14f0e999617c96e3d52) | Complex number of 2 32-bit big-endian IEEE floating point numbers   
[H5T_COMPLEX_IEEE_F32LE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_c_o_m_p_l_e_x.html#ga195a2f2f9614f855d21090e4fbff9f04) | Complex number of 2 32-bit little-endian IEEE floating point numbers   
[H5T_COMPLEX_IEEE_F64BE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_c_o_m_p_l_e_x.html#ga88831575ae080e95865edb0aaa7ee6ad) | Complex number of 2 64-bit big-endian IEEE floating point numbers   
[H5T_COMPLEX_IEEE_F64LE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_c_o_m_p_l_e_x.html#ga492b3488326a498233ab8e6ad8d38719) | Complex number of 2 64-bit little-endian IEEE floating point numbers   
[H5T_FLOAT_BFLOAT16BE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_a_l_t_f_l_o_a_t.html#ga4dd1e86cccbdcf1c22fddbf6ad88057e) | 16-bit big-endian bfloat16 floating point   
[H5T_FLOAT_BFLOAT16LE](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_a_l_t_f_l_o_a_t.html#ga8fb1cbb4415c84c04663040597ffc009) | 16-bit little-endian bfloat16 floating point   
[H5T_FLOAT_F8E4M3](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_a_l_t_f_l_o_a_t.html#ga8cfa202d0101ec59d2f270d0d5645c58) | 8-bit FP8 E4M3 (4 exponent bits, 3 mantissa bits) floating point   
[H5T_FLOAT_F8E5M2](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_a_l_t_f_l_o_a_t.html#gaf2e1617cdd3d211350dd9414af1ff00f) | 8-bit FP8 E5M2 (5 exponent bits, 2 mantissa bits) floating point   
[H5T_NATIVE_DOUBLE_COMPLEX](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_n_a_t.html#ga00cdc9734afbfead614191bd9736bc37) | double _Complex (MSVC _Dcomplex)   
[H5T_NATIVE_FLOAT_COMPLEX](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_n_a_t.html#ga957f6b409daca9447dfcf671c9b18610) | float _Complex (MSVC _Fcomplex)   
[H5T_NATIVE_LDOUBLE_COMPLEX](https://support.hdfgroup.org/documentation/hdf5/latest/group___p_d_t_n_a_t.html#ga841b6107417a1bb8bae085333ee7a6c8) | long double _Complex (MSVC _Lcomplex)   
[H5VL_NATIVE](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_v_lnative_8h.html#a3198509e19c60950ab0045b089816118) | Identifier for the native VOL connector   
H5VL_PASSTHRU  | Identifier for the pass-through VOL connector   
List of removed public APIs
Function   
---  
[H5Dread_chunk()](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#a8ff3b0cf52e30e2e12d617aa2329486e)  
H5FDperform_init()   
[H5Iregister_type()](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#af51df104e1e3ff0b99b7a8ca368f14ab)  
[H5Tdecode()](https://support.hdfgroup.org/documentation/hdf5/latest/_h5version_8h.html#ac90f7722dacad861c0a22507d3adf0dd)  
H5VLpeek_connector_id_by_name()   
H5VLpeek_connector_id_by_value()   
H5VLfinish_lib_state()   
H5VLstart_lib_state()   
* * *
Navigate back: [Main](https://support.hdfgroup.org/documentation/hdf5/latest/index.html) / [Release Specific Information](https://support.hdfgroup.org/documentation/hdf5/latest/release_specific_info.html) / [Release Specific Information for HDF5 2.0](https://support.hdfgroup.org/documentation/hdf5/latest/rel_spec_20.html)
  * Generated by [![doxygen](https://support.hdfgroup.org/documentation/hdf5/latest/doxygen.svg)](https://www.doxygen.org/index.html) 1.13.2 


