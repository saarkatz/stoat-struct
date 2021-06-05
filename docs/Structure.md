# Structures
When defining a class of the Structure type we want to collect all the
members of the Structure type and define the structure of the class.
When an instance of the class is created we want to initialize all its
substructures recursively the get the complete structure.

## Usage
Structures have two modes of operation.
1. As Data Source
2. As Compound Structure

**As data source** the structure supplies the methods to write and
retrieve its data. \
**As compound structure** the structure simply
contains other structures.

In theory the two modes can be combined and exists within the same
class.
 
## Internals
### Construction
When a new class in defined it is constructed from the structures inside
it.

Using a custom dictionary type, which we will call the _constructor_,
returned by the `__prepare__` method of the metaclass, we collect all
the items that are of a structure type.  
Using the `__getitem__` method of the constructor we can turn every
access to one of the internal structures within the definition of the
class to a named reference. This will help us create internal
connections that will help up with structure such as dynamic arrays.  
Within the `__new__` method of the metaclass the blueprint of the class
is generated along with a table of connections between members of the
class. These connections will be generated based on the connection
requests from partial structures. Partial structure will be any
structure that requires an external connection to be complete and
functional such as a dynamic array that requires the size.  
In addition properties will be made for each of the items that are
structures. 

Each new class will be assigned an unique id and registered in a class
registry with the id and a configuration as the key. When a new class
will be created by method of reconfiguration it will have the same id
with a different configuration.  
This configuration exists to allow classes that have similar behaviors
that differ in only parameters to be implemented only once.  
The registry will allow a reconfiguration to return the same class type
every time an identical configuration is used. (Here special care will 
be required to avoid memory leaks by creating large number of classes - 
maybe release the classes when there are no more instances of them?)  
The configuration will is a custom made validator to ensure the values
of the configuration are as intended.

### Initialization
When a structure class is called it will instantiate an instance of
itself from the blueprint defined in the construction. Each internal
structure will be initialized recursively and saved in a data collection
within the instance.  
Any partial structure class will then be completed
by making its requested connection (Here care should be exercised in
the case of a partial structure that requires values from another
partial structure. There is currently no use case for such a thing but
it is theoretically possible).

### Components
| Name            | Internal? | Description                        |
| --------------- | --------- | ---------------------------------- |   
| MetaStructure   | Yes       | The metaclass enabling the structure functionality. |
| Constructor     | Yes       | Custom dict-like class that will provide the `__getitem__` enabling dynamic item references within a class. |
| Reference       | Yes       | The class that will be returned by the constructor to indicate references. |
| Registry        | Yes       | A singleton class that will be responsible to managing the class registry. |
| Accessor        | Yes       | Property constructor that generates the access properties for the members of a structure. |
| Connection      | Yes       | The class that will represent the connection requests of partial structures. |
| Configuration   | No        | A rule based system for defining the configurations of the classes. This system might be used by a user to define a costume class. |
| ConfigBuilder   | No        | An auxiliary system that will hide the dictionary nature of the configuration from the user. Ideally this will be derivable from the configuration |
| Structure       | No        | The class that will be inherited to allow the creation of structures. |
| Array           | Yes       | A special structure that will implement the array functionality. Comes with two modes - static and dynamic. |
