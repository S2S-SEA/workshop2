'''

This is exercise 3 
It is based on counting the number of dry days shown in the presentation

'''

## Dry days example 

Sing_Rain = [13.3, 0, 0, 0, 1,10.7, 0.2]

dry_days_v1= 0	
		
for i in range(7):			
	print('Location '+ str(i))	
	if Sing_Rain[i] <1:	
		dry_days_v1+= 1	
print('The number of dry days, version 1: ' + str(dry_days_v1))			

dry_days_v2= 0	# starting with a different name, since plotting out the two examples
		
for i in range(7):			
    print('Location '+ str(i))		
if Sing_Rain[i] < 1:	
		dry_days_v2+= 1	
print('The number of dry days, version 2: ' + str(dry_days_v2))	