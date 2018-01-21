# The Groundr Project
###### Inspired by LabelMe

It is well established that Machine Learning solutions require large amounts of labelled data to 'train' themselves. Data rarely comes labelled however, and so any team that wishes to deploy a Machine Learning solution will have to write a program to label the data for them or do it manually. This is a signficant expendature of resources that is often repeated with each new solution. The Groundr project seeks to provide a unified tool set to label data in a quick and user friendly fashion. Users can upload their image libraries, organize them into directories of their choice, and begin labelling the images. The labelling interface supports indicating a region of interest and assigning multiple attributes or labels to it. This information is automatically saved as a json file and stored alongside the image. The software automatically cycles the user through the directory until there are no more images without json files. Users can access each file individually as they see fit and edit their labels. 

The entire system is hosted by each institution on their own servers. 

### Build Status:
Version 0.0.1 Building properly. 

### Code Style: Standard

### Built with:
* AngularJS
* Flask 

## Installation:

Installation is quick and straightforward:

```
Clone the above repo onto your server of choice. 
If you wish to change which ports and host location the UI is displayed at, make those changes in the main.py file at the top. 
In server console type 'flask run'.
Enjoy!
```
## How to Use:

Once the server is running, you can access the UI by visiting the website at the location you specified or at the defaults:

```
host: 0.0.0.0
port: 5000
```

By going to this address in your web-browser of choice, you will be presented with the home screen. From here you can select view images, check your templates, or select directories. Viewing images allows you to upload or label already present images in the directories. 

Selecting directories allows you to see your current file structure and everything contained within it. It also allows you to edit said file structure. 

Selecting Template will allow you to access your templates. Currently, every directory is required to have their own templates. These templates provide guides for those labelling your data. You can only assign labels that are present on the template to an image. This was introduced to prevent possible typos and mispellings on the user end that can result in a loss of data. Templates can be edited at any time. The templates are directory based, that is, only one template is present in each directory. 

Labelling images is intuitive, allowing users to construct regions of interests using a connect-the-dots based system where a user defines a region by placing points marking its edges.

## Contribute:

Further development should be directed towards improving the user interface and introducing further utilities. A current TODO list is as follows:

* In-house algorithm that automatically selects regions of interest and labels data on its own
* Search tool to search for images by label
* Improved User Interface
* Delete old Docker Containers in Demo. 
* Add PHP to make it look nice and react to changes (such as previewing the file name when uploading)

Credits:
Machine Intelligence Lab, University of Florida
Kevin - Lead Software Developer
Daniel - Lead Software Developer
Nicholas - Software Developer
Steven - Software Developer