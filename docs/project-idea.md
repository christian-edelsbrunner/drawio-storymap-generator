# Project Idea
I want a tool that takes a hierarchy of "cards" as yaml and creates a draw.io diagram file containing a Story map for this this 

# Architecture: 
* We have an internal Data Model for the Story Map containing the relevant items
* On the import side we can import yaml structure of cards for now (later on also other formats so we need it to be loosly coupled)
* On the output side we are able to generate draw.io diagrams using drawpyo - but want also to support other formats later on
For the beginning the tool should be a CLI but later on could also be hosted somewhere in an OCI image

