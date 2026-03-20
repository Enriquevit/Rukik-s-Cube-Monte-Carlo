# OLL & PLL — Status & Technical Reference

## Overview

**OLL (Orientation of the Last Layer)** and **PLL (Permutation of the Last Layer)** are stages 3 and 4 of CFOP. After F2L, only the last layer (D/yellow) remains unsolved.

- **OLL** orients all D-layer pieces so yellow stickers face downward (all on the D face).
- **PLL** permutes the D-layer pieces into their correct positions without disrupting orientation.

### Cube3.py Orientation


Standard OLL/PLL algorithms assume yellow = U (last layer on top). Since our last layer is on D, all algorithms are converted with an **x2 rotation**:

