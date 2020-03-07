# stoat
## How to Use Stoat
To create a structure, simply inherit from Structure
```python
from stoat.structure import Structure
from stoat.cstructure import Int, Short, Char

class Label(Structure):
    id = Int+'<'
    name_size = Short
    name = Char['name_size']

label = Label()
label.id = 1234
label.name_size = 7
label.name = b'MyLabel'

binary_data = label.pack()
label2 = Label.unpack(binary_data)
```
