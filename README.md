## GraphV

GraphV is a program writted in python to create and visualise collaboration graphs of universities. Data of eployees and their coauthors is based on science publications gathered from Google Scholar.
# Installation

To open the program run the Main.py file with your python2.7 interpreter.

If there is a problem with import errors, use PIP or apt-get command to install them.
Graph Tool installation

For Ubuntu, add the following lines in /etc/apt/sources.list :

deb http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION universe
deb-src http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION universe

where DISTRIBUTION can be any one of xenial, yakkety, zesty After running apt-get update, the package can be installed with

apt-get install python-graph-tool

If you want to verify the packages, you should use the public key 612DEFB798507F25, which can be done with the command:

apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25

Usage

Import the databes (You can find it in Resources) to Your MySql.

After You run the program connect with Your MySql database with Your imported database.
Contributing

Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request

Created by

Created by Patrick Rutkowski. If You have any questions contact with me by mail: colalightoriginal@gmail.com
License

Open Source
