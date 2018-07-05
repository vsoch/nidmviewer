# nidm-viewer

NIDM Results Viewer

 - parses peak coordinates and associated brain maps
 - interactive coordinate browsing
 - save image to file (export)
 - produces html code for embedding, or local viewer
 - uses [font brain](http://vsoch.github.io/font-brain) for nidm and brain imaging icons


## Documentation
Complete documentation [is available](http://nidmviewer.readthedocs.org/en/latest/)

### Installation
To install

```
pip install nidmviewer
```

To install development version:
```
pip install git+git://github.com/vsoch/nidmviewer.git
```

### Running Examples

#### Command Line

When installing with setup.py, an executable, `nidmviewer` is installed in your bin to view nidm files on the fly. Here we will run an example using a local file (nidm.ttl) for which the excursion set maps are served from a webserver (neurovault) and the full paths represented in the `excsetmap_location` parameter in the turtle file.  This use case coincides with downloading a nidm.ttl and wanting to look at (remotely hosted) maps.

```
nidmviewer neurovault/nidm.ttl --port 8833
Starting up the nidmviewer!
Found results matching query.
/tmp/tmpuwfuszb9
Serving nidmviewer at port 8833
127.0.0.1 - - [24/Jan/2018 12:03:43] "GET /pycompare.html HTTP/1.1" 200 -
Created new window in existing browser session.

```

The browser should open up automatically to the url.

But what if you have an entire (local) set of nidm files and images? We have a lot of images locally in the fsl folder:

```
ls fsl/
ContrastStandardError_T001.nii.gz  DesignMatrix.csv          GrandMean.nii.gz                 MNI152_T1_2mm_brain.nii.gz       rendered_thresh_zstat1.png  TStatistic_T001.nii.gz
ContrastStandardError_T002.nii.gz  DesignMatrix.png          index.html                       MNI152_T1_8mm_brain_mask.nii.gz  rendered_thresh_zstat2.png  TStatistic_T002.nii.gz
Contrast_T001.nii.gz               ExcursionSet_T001.nii.gz  Mask.nii.gz                      nidm.provn                       ResidualMeanSquares.nii.gz  ZStatistic_T001.nii.gz
Contrast_T002.nii.gz               ExcursionSet_T002.nii.gz  MNI152_T1_2mm_brain_mask.nii.gz  nidm.ttl                         SearchSpaceMask.nii.gz      ZStatistic_T002.nii.gz
```

and if you look in the [examples/fsl/nidm.ttl](examples/fsl/nidm.ttl) you will see paths to files. If you naively try to serve them from (somewhere other than the same folder they live in) you are going to get a bunch of 404s. Please cd into the folder before you do this, so the web root is where the files are found:

```
nidmviewer fsl/nidm.ttl --port 8811
```

![img/example.png](img/example.png)


You can see the basic usage by typing the command:
 
```
usage: nidmviewer [-h] [--base BASE] [--port PORT]
                  [--columns_to_remove COLUMNS_TO_REMOVE]
                  ttl

command line or server tool to view or compare nidm results.

positional arguments:
  ttl                   List of comma separated ttl files to parse.

optional arguments:
  -h, --help            show this help message and exit
  --base BASE           base image (standard brain map) to use for the viewer
                        background.
  --port PORT           PORT to use to serve nidmviewer (default 8088).
  --columns_to_remove COLUMNS_TO_REMOVE
                        Comma separated list of columns to remove from viewer.
usage: nidmviewer [-h] [--base BASE] [--port PORT]
                  [--columns_to_remove COLUMNS_TO_REMOVE]
                  ttl

command line or server tool to view or compare nidm results.

positional arguments:
  ttl                   List of comma separated ttl files to parse.

optional arguments:
  -h, --help            show this help message and exit
  --base BASE           base image (standard brain map) to use for the viewer
                        background.
  --port PORT           PORT to use to serve nidmviewer (default 8088).
  --columns_to_remove COLUMNS_TO_REMOVE
                        Comma separated list of columns to remove from viewer.
```

If you need more substantial customization, it's recommended to use the python functions to generate your own
html.

#### Python
see [an example](examples/generate_viewer.py). This example will generate a snippet of code that you can save as an `index.html` file, and will render served alongside the images in the [examples/fsl](examples/fsl) folder.


###### Many Thanks
 - [Papaya Viewer](https://github.com/rii-mango/Papaya), we salute you!
 - [NeuroVault](https://github.com/NeuroVault/NeuroVault) don't mess with the NeuroVault!

please [submit feedback and requests](https://github.com/vsoch/nidmviewer) or see the [demo](http://vsoch.github.io/nidmviewer)
