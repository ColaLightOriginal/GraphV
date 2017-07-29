# GraphV

GraphV is a program writted in python to create and visualise collaboration graphs of universities. Data of eployees and their coauthors is based on science publications gathered from Google Scholar.

## Prerequisites

Prerequisites to rune the program:
* Ubuntu OS
* Python 2.7
* MySql with MySql Workbench

## Installation

First add repository to source list:

``` echo "deb http://downloads.skewed.de/apt/xenial xenial universe" >> /etc/apt/sources.list```

```echo "deb-src http://downloads.skewed.de/apt/xenial xenial universe" >> /etc/apt/sources.list```

Add a new public key:
```apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25```

After that, install all the necessary dependencies like graph-tool, matplotlib, sql-connector, cairo and numpy with 
Dependencies Installer file:

```sudo ./Dependencies_Installer```

If there is a problem with import errors, use PIP or apt-get command to install them.

## Run

To open the program use RUN file:

```./RUN```

## Usage

* Import the databes files (UMKnotPrecise_coauthors.sql, UMKnotPrecise_employess) to Your MySql.
* After You run the program connect with Your MySql database (button Connect).
* Fill the fielfs: Database name (UMKnotPrecise) Username, Host, Password.
* Wait a minute for graph to generate.
* Program is ready to use

## Issues

On the Widget window there is a problem with render after using a scroll. To see all the edges and nodes after You use scroll, click ont the filter option '=1'. 

## Contributing

Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request

## Created by

Created by Patrick Rutkowski. If You have any questions contact with me by mail: colalightoriginal@gmail.com
## License

Open Source
