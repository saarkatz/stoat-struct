# stoat
## How to Use Stoat
To create a structure, simply inherit from Structure

```python
from stoat.core import Structure
from stoat.stypes import Int, Short, Char, Config

class Label(Structure):
    id = Int < Config.Endianness.Little
    name_size = Short
    name = Char[name_size]

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
coverage run --source src -m pytest
```
