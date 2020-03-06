# TODOs
* Add label/grouping syntax
```python
```python
from stoat import Structure
from stoat.CStructure import Char, Short

class MyStruct(Structure):
    # Option 1
    class group1(Strcuture):
        a = Char
        b = Short
        
    # Option 2
    group2 = Structure(
        a = Char,
        b = Short
    )
    
    # Option 3
    group3 = {
        'a': Char,
        'b': Short
    }
    
    # Option 4
    group4: Structure(
        a = Char,
        b = Short
    )
    
    
    # Option 5
    group5: {
        'a': Char,
        'b': Short
    }
```
* Add class definition checks - Remove runtime checks and improve
  performance
* Add compound byte field structure (One byte divided among several fields)
* Add Type access casting (Have a char be viewed as an integer)
* Add constant structure (A field that always has the same value)
* Add reflection structure (A structure that reflects the value of
  another structure)
* Add conditional structure (Functions as one of several structure
  depending on a condition)?
* Choose an original name for the project (StructureAnt - strant)