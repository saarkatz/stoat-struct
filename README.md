# stoat
## How to Use Stoat
To create a structure, simply inherit from Structure

```python
from stoat.core.structure import Structure
from stoat.core.utils import params
from stoat.types.ctypes import Int32, Int16, Char
from stoat.types.ctypes.params import Endianness

class Label(Structure):
    id: Int32 = params(endianness=Endianness.Little)
    name_size: Int16
    name: Char[this.name_size]

label = Label()
label.id = 1234
label.name_size = 7
label.name = b'MyLabel'

binary_data = label.pack()
label2 = Label.unpack(binary_data)
```

## Test
At the project directory run the command:
```shell script
coverage run --source src -m pytest --ignore=old
```
