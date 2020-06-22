import numpy as np
import pandas as pd
import os, sys

df = pd.read_csv("scenes/v9_scenes_stats.csv", skiprows=1) 

print("hsv change per frame: ", np.mean(df['content_val']))



