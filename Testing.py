import numpy as np
import pandas as pd


df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6]]))
print(df)
# Use the `shape` property
print(df.shape)

# Or use the `len()` function with the `index` property
print(len(df.index))