'''
Dealing with Arrays example

numpy functions that may be useful:

np.mean(arrayname)  # this averages over the whole array 
np.mean(arrayname, axis = 0) # this averages over only the first axis.
np.shape(arrayname) # this out puts the shape of the array
np.sum(arrayname) # adds up the values in the array
np.sum(arrayname, axis=1) # adds up only the values on the second axis. 
'''

import numpy as np

Jun_2018_precip =np.array([[102.0,98.8], 
			        [94.2 , 75.4],
			        [88.6, 64.2], 
			        [72.8, 34.8]]) 


Jun_Jul_2018_precip = np.array([ [[102.0, 80.4], [98.8, 80.6]],
 			[[94.2, 84.6], [75.4, 90.8]], 
			[[88.6, 74.2], [64.2, 62.2]], 
			[[72.8, 55.8], [34.8, 46.6]] ])



#Print out the size of the two arrays below:
print('The size of the Jun_2018_precip array is:')

print('The size of the Jun__Jul_2018_precip array is:')



#Print out the average June precipation for the 8 locations
print('The average June precipitation was:')


#Print out the average July precipitation for the 8 locations
print('The average July precipitation was:')



#Print out the total average precipation for June and July. 
#Challenge to do so in one line using np.mean once and np.sum once. 
print('The total average precipation for June and July was:')

