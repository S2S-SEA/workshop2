'''
Dealing with Arrays example

numpy functions that may be useful:

np.mean(arrayname)  # this averages over the whole array 
np.mean(arrayname, axis = 0) # this averages over only the first axis.


'''

import numpy as np

Jan_2016_precip =np.array([[102.0,98.8], 
			        [94.2 , 75.4],
			        [88.6, 64.2], 
			        [72.8, 34.8]]) 


Jan_Feb_2016_precip = np.array([ [[102.0, 80.4], [98.8, 80.6]],
 			[[94.2, 84.6], [75.4, 90.8]], 
			[[88.6, 74.2], [64.2, 62.2]], 
			[[72.8, 55.8], [34.8, 46.6]] ])
