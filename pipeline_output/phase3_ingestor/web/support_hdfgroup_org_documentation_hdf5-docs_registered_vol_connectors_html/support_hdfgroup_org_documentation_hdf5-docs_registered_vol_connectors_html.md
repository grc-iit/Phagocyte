[![Logo](https://support.hdfgroup.org/assets/img/The_HDF_Group_stackedlogo.png)](https://www.hdfgroup.org/)
  * [The HDF Group](https://www.hdfgroup.org/)
  * [Downloads](https://support.hdfgroup.org/downloads/index.html)
  * [Documentation](https://support.hdfgroup.org/documentation/index.html)
  * [Community Forum](https://forum.hdfgroup.org)
  * [Licenses](https://www.hdfgroup.org/licenses)
  * [Help Desk](https://help.hdfgroup.org)
  * [HDF Software Priority Support](https://www.hdfgroup.org/solutions/priority-support/)
  * [HDF Consulting](https://www.hdfgroup.org/solutions/consulting/)
  * [Archive](https://support.hdfgroup.org/archive/support/index.html)
  * [Search](https://support.hdfgroup.org/search.html)

  

### Got HDF5?
[![Visualization of an HDF5 file](https://support.hdfgroup.org/assets/img/view-HDF5-file-in-browser.png)](https://myhdf5.hdfgroup.org/)   
Curious to see what’s inside? Try [this](https://myhdf5.hdfgroup.org/)
(This free tool will show you the contents of an HDF5 file in your browser, without any data leaving your computer! For more info, check out [H5Web](https://h5web.panosc.eu/).)
# Registered VOL Connectors
Members of the HDF5 users community can register VOL connectors for use with HDF5. To register a VOL connector please contact [The HDF Helpdesk](https://help.hdfgroup.org) with the following information:
  * Contact information for the developer requesting a new identifier
  * Short description of the new connector
  * Links to any relevant information including licensing information


Here is the current policy regarding VOL connector identifier assignment: Valid VOL connector identifiers can have values from 0 through 255 for connectors defined by the HDF5 library. Values 256 through 511 are available for testing new VOL connectors. Subsequent values should be obtained by contacting the [The HDF Help Desk](https://help.hdfgroup.org).
Please contact the maintainer of a VOL connector for help implementing the plugin.
## List of VOL Connectors Registered with The HDF Group
Connector | Connector Identifier | Search Name* | Short Description | URL | Contacts  
---|---|---|---|---|---  
Asynchronous I/O | 512 | async | Provides support for asynchronous operations to HDF5 | <https://github.com/hpc-io/vol-async> | Suren Byna (sbyna at lbl dot gov)  
Cache | 513 | cache | Provides support for multi-level, multi-location data caching to dataset I/O operations | <https://github.com/hpc-io/vol-cache> | Suren Byna (sbyna at lbl dot gov)  
Log-based | 514 | LOG | The log-based VOL plugin stores HDF5 datasets in a log-based storage layout.  
In this layout, data of multiple write requests made by an MPI process are appended one after another in the file. Such I/O strategy can avoid the expensive inter-process communication and I/O serialization due to file lock contentions when storing data in the canonical order. Through the log-based VOL, existing HDF5 programs can achieve a better parallel write performance with minimal changes to their codes. | <https://github.com/DataLib-ECP/vol-log-based/blob/master/README.md> | Kai Yuan Hou   
(khl7265 at ece dot northwestern dot edu)  
DAOS | 4004 | daos | Designed to utilize the DAOS object storage system by use of the DAOS API   
https://doi.org/10.1109/TPDS.2021.3097884 |  <https://github.com/HDFGroup/vol-daos>   
[HDF5 DAOS VOL Connector Design](https://github.com/HDFGroup/vol-daos/blob/master/docs/design_doc.pdf)   
[HDF5 DAOS VOL Connector User’s Guide](https://github.com/HDFGroup/vol-daos/blob/master/docs/users_guide.pdf) | help at hdfgroup dot org  
native | 0 | native |  |  | help at hdfgroup dot org  
pass-through | 517 | pass_through_ext | Provides a simple example of a pass-through VOL connector | <https://github.com/hpc-io/vol-external-passthrough> | Suren Byna (sbyna at lbl dot gov)  
dset-split | 518 | dset-split | Creates separate sub files for each dataset created and mounts these sub-files as external links in the main file. It enables versioning of HDF5 files at a dataset boundary. | <https://github.com/hpc-io/vol-dset-split> | Annmary Justine (annmary dot roy at hpe dot com)  
PDC-VOL | 519 | PDC-VOL | It is a terminal VOL that reads and writes HDF5 objects to the PDC system |  <https://github.com/hpc-io/pdc> <https://github.com/hpc-io/vol-pdc> | Houjun Tang (htang4 at lbl dot gov)  
REST | 520 | REST | Designed to utilize web-based storage systems by use of the HDF5 REST APIs | <https://github.com/HDFGroup/vol-rest> | Matthew Larson (mlarson at hdfgroup dot org)  
LowFive | 521 | LowFive | A new data transport layer based on the HDF5 data model, for in situ workflows. Executables using LowFive can communicate in situ (using in-memory data and MPI message passing), reading and writing traditional HDF5 files to physical storage, and combining the two modes. | <https://github.com/diatomic/LowFive> | Tom Peterka (tpeterka at mcs dot anl dot gov)   
Dmitriy Morozov (dmorozov at lbl dot gov)  
*The Search Name provides a mechanism for searching for a VOL.
## List of Prototype VOL Connectors
Connector | Connector Identifier | Search Name* | Short Description | URL | Contacts  
---|---|---|---|---|---  
rados | unassigned | rados | Prototype VOL connector to access data in RADOS | <https://github.com/HDFGroup/vol-rados> | help at hdfgroup dot org  
*The Search Name provides a mechanism for searching for a VOL.
