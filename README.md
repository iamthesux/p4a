sqp
===

An Arma config parser for python

###Features

- parses sqm and biedi files into usable data structures
- outputs properly formatted and indented code


###Possible Uses

* You need to convert a biedi file to sqm or vice versa with a little 
  more control than the existing tools offer.

* You have a large set of missions, and you want to rename, upgrade or 
  otherwise modify them in some meaningfull way.
  
* You have a mission with 100 players and need to append some init code
  to every one.  See player_example.py

###Installation

You will need python 2.7 or greater (but not 3).  Simply copy sqp.py to
wherever you need it, then write your script there or use the python shell.

###Usage

See the two examples provided or refer to the in-source documentation.

###Limitations

* Does not support hpp files yet.  If there is interest I can easily add
  this feature.
* It may or may not detect syntax errors.
* Comments are currently not supported and will cause it to break
* Not thoroughly tested, use caution overwriting your files.