# py-structure
## How to Use PyStructure
To create a structure, simply inherit from Structure
```python
from old.py_structure import Structure, Int, Short, Char

class Label(Structure):
    id = Int+'LE'
    name_size = Short
    name = Char['name_size']

label = Label()
label.id = 1234
label.name_size = 7
label.name = 'MyLabel'

binary_data = label.pack()
label2 = Label.unpack(binary_data)
```

## How a Structure Works
### The General Idea
When defining a class of the Structure type we want to collect all the
members of the Structure type and define the structure of the class.
When an instance of the class is created we want to initialize all its
substructures recursively the get the complete structure.

### The Implementation Idea
Structures have two modes of operation.
1. As Data Source
2. As Compound Structure

**As data source** the structure supplies the methods to write and
retrieve its data. \
**As compound structure** the structure simply
contains other structures.

Upon definition, a compound structure will define its structure, saved
in the variable `_c_structure`. Any additional information required by
the members of the compound structure but that is not part of its
members would be saved in the variable `_c_data`.  
When initializing an instance, the data for the internal structures will
be saved in the variable `_i_data`.

Both data variables are not directly accessed by be the class members
but instead are passes to them whenever relevant.  
The data will be in the form of dictionaries that will always be passed
by expansion. This way any function receiving the data will be able to
use default values as well as be used manually. These two thing are
especially relevant in the case of initialization which can happen
internally in a compound structure or manually when creating instances
of the relevant classes.

One important feature of the structure would be the ability to generate
arrays of existing types with no additional implementation. To allow for
dynamic arrays, an array type will have to have access to the variable
containing its size. The path to the required variable would be defined
in the variable `_c_data` along with any data required for its internal
data type.

### Definitions
A **Structure** is a class that inherits the Structure class and
implements at least on of the data source mode or the compound structure
mode.

A **Type** is a Structure along with all the data required for its
initialization.

A **Factory** is an instance of the TypeFactory class the encapsulates
the structures and holds the data required to turn these structures to
types.
