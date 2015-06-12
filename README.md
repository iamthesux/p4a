p4a
===

A collection of tools for working with the Real Virtuality engine.

###Features

- can parse both text and binary rap formats
- outputs rap data as formatted text
- allows manipulation of rap data within python
- parses pbo


###Possible Uses

* You need to convert a biedi file to sqm or vice versa with a little 
  more control than the existing tools offer.

* You have a large set of missions, and you want to rename, upgrade or 
  otherwise modify them in some meaningfull way.
  
* You have a mission with 100 players and need to append some init code
  to every one and ensure they are playable.

###Installation

Install directly from github with pip:
```
pip install https://github.com/iamthesux/p4a/archive/master.zip
```

###Usage

See the two examples provided or refer to the source.

###Limitations

* It may or may not detect syntax errors.
* Comments and preprocessor are currently unsupported and will cause it to break
* Not thoroughly tested, use caution overwriting your files.
