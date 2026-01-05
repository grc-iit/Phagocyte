[[Index]](https://support.hdfgroup.org/documentation/hdfview/latest/index.html) [[1]](https://support.hdfgroup.org/documentation/hdfview/latest/ug01introduction.html) [[2]](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html) [[3]](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html) [[4]](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html) [[5]](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html) [[6]](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html) [[7]](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html)
# HDFView User's Guide
_**This document is a user's guide on how to use HDFView.**_
* * *
HDFView is a graphic utility designed for viewing and editing the contents of HDF4 and HDF5 files. This document provides the following information:
  * User instructions for HDFView
  * A brief discussion of the HDF object model (Details of the HDF object model are available from [HDF Object Package](https://support.hdfgroup.org/documentation/hdfview/latest/javadocs/hdfview_java_doc/hdf/object/package-summary.html).)


* * *
## Table of Contents
  * [Chapter 1: Introduction](https://support.hdfgroup.org/documentation/hdfview/latest/ug01introduction.html)
    * [1.1 Overview](https://support.hdfgroup.org/documentation/hdfview/latest/ug01introduction.html#ug01overview)
    * [1.2 About This Release](https://support.hdfgroup.org/documentation/hdfview/latest/ug01introduction.html#ug01release)
    * [1.3 Further Information](https://support.hdfgroup.org/documentation/hdfview/latest/ug01introduction.html#ug1furtherinfo)
  

  * [Chapter 2: Getting Started](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html)
    * [2.1 The Main Window](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html#ug02main)
    * [2.2 Opening a File](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html#ug02load)
    * [2.3 Tree View of File Hierarchy](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html#ug02tree)
    * [2.4 Status Information](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html#ug02message)
    * [2.5 Viewing HDF Metadata](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html#ug02property)
    * [2.6 Command-line Options](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html#ug02option)
  

  * [Chapter 3: HDF Object Model](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html)
    * [3.1 Overview](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html#ug03overview)
    * [3.2 The HDF Object Package](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html#ug03definition)
    * [3.3 Class Hierarchy](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html#ug03hierarchy)
    * [3.4 Using the HDF Object Package](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html#ug03application)
  

  * [Chapter 4: The Tree Viewer](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html)
    * [4.1 Overview](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04overview)
    * [4.2 Tree Structure](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04tree)
    * [4.3 View Data Content](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04data)
      * [4.3.1 Show Bit Values](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04bitmask)
    * [4.4 Display Metadata and Attributes](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04metadata)
    * [4.5 Edit File and File Structure](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04edit)
      * [4.5.1 Create and Save File](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04file)
      * [4.5.2 Setting the Library version bounds](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04libversion)
      * [4.5.3 Add and Delete Object](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04add)
      * [4.5.4 Copy and Paste Object](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04copy)
      * [4.5.5 Move Object](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04move)
      * [4.5.6 Add, Delete and Modify Attribute](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html#ug04attribute)
  

  * [Chapter 5: Table Viewer](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html)
    * [5.1 Open Dataset](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05display)
    * [5.2 Subset and Dimension Selection](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05subset)
      * [5.2.1 Setting Valid Values](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05range)
      * [5.2.2 Dimension Size](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05subset_size)
      * [5.2.3 Three or More Dimensions](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05subset_3d)
      * [5.2.4 Swap Dimension and Data Transpose](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05subset_transpose)
      * [5.2.5 Compound Dataset Options](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05subset_compound)
    * [5.3 Display a Column/Row Line Plot](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05lineplot)
    * [5.4 Change Data Value](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05change)
    * [5.5 Save Data Values to a Text File](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05save)
    * [5.6 Import Data from a Text File](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05import)
    * [5.7 Dataset storing references](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05datasetreferences)
      * [5.7.1 Dataset Storing Object References](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05objectref)
      * [5.7.2 Dataset Storing Dataset Region References](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05regionalref)
    * [5.8 Save Data Values to a Binary File](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05savebinary)
    * [5.9 Import Data from a Binary File](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html#ug05importbinary)
  

  * [Chapter 6: Image Viewer](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html)
    * [6.1 Display a 2-D or 3-D Image](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06image)
      * [6.1.1 Indexed Image (8-Bit)](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06image_indexed)
      * [6.1.2 True Color Image](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06image_true)
    * [6.2 Zoom/Flip/Contour Image](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06zoom)
    * [6.3 Animation](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06animation)
    * [6.4 View and Modify Image Palette/Values](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06palette)
    * [6.5 Show Histogram of Pixel Values](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06histogram)
    * [6.6 Import JPEG, GIF, PNG, or BMP Image to HDF4/5](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06import)
    * [6.7 Save HDF Image to JPEG, GIF, PNG, or BMP File](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html#ug06save)
  

  * [Chapter 7: User Options](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html)
    * [7.1 General Settings](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07general)
      * [7.1.1 Working Directory](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07directory)
      * [7.1.2 User's Guide Path](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07help)
      * [7.1.3 File Access Mode](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07fileaccess)
      * [7.1.4 Text Font](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07font)
      * [7.1.5 Image Options](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07imageopt)
      * [7.1.6 Data Options](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07dataopt)
      * [7.1.7 Number of Open Objects](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07objectcount)
    * [7.2 HDF Settings](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07hdf)
      * [7.2.1 File Extensions](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07extension)
      * [7.2.2 Library Versions](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07libversion)
      * [7.2.3 Data Options](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07dataopt)
      * [7.2.4 Display Indexing](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html#ug07displayind)
* * *
[[Index]](https://support.hdfgroup.org/documentation/hdfview/latest/index.html) [[1]](https://support.hdfgroup.org/documentation/hdfview/latest/ug01introduction.html) [[2]](https://support.hdfgroup.org/documentation/hdfview/latest/ug02start.html) [[3]](https://support.hdfgroup.org/documentation/hdfview/latest/ug03objects.html) [[4]](https://support.hdfgroup.org/documentation/hdfview/latest/ug04treeview.html) [[5]](https://support.hdfgroup.org/documentation/hdfview/latest/ug05spreadsheet.html) [[6]](https://support.hdfgroup.org/documentation/hdfview/latest/ug06imageview.html) [[7]](https://support.hdfgroup.org/documentation/hdfview/latest/ug07useroptions.html)
* * *


