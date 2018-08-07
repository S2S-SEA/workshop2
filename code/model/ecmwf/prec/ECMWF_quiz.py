'''
Quiz
'''

print('Welcome to the S2S data structure quiz')
name = input('What is your name?')
print('Hi there '+ name + "! Let's play a game!")
print('I will ask you 10 questions. Mix of Multiple choice and enter yourself')
print('Please keep caps lock on so all answers can be printed in caps')
print('All dates must be in the format DD-MM-YYYY')
print('-----------------------------------------------------------------')
score = 0.0


print('Question 1: What is the first ECMWF December model run in December 2017?')
print('A: 01-12-2017')
print('B: 03-12-2017')
print('C: 09-12-2017')
print('')

Q1answer = "B"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again. Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. ECMWF S2S forecasts are produced on Mondays and Thursdays. The first Monday or Thursday in December 2017 was 03-12-2017')

print('')
print('Question 2: What is the first ECMWF December model run in August 2018?')
print('A: 01-08-2018')
print('B: 02-08-2018')
print('C: 03-08-2018')
print('')

Q1answer = "B"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again. Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. ECMWF S2S forecasts are produced on Mondays and Thursdays. The first Monday or Thursday this month was 02-08-2018')

print('')
print('Question 3: I want to get the weekly forecast starting the 13-08-2018. What ECMWF model run should I use to find the lead time 1 forecast?')
print('Enter the date in the format DD-MM-YYYY')
print('')

Q1answer = "13-08-2018"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again. Remember to answer in DD-MM-YYYY.')
    Q1response = input('Your answer : ')
print('Well done. Lead Time 1 starts from the first day of the week.')

print('')
print('Question 4: I want to get the weekly forecast starting the 13-08-2018. What ECMWF model run should I use to find the lead time 2 forecast?')
print('A: 06-08-2018')
print('B: 13-08-2018')
print('C: 20-08-2018')
print('')

Q1answer = "A"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again. Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. Lead Time 2 starts from the week before first day of the week.')


print('')
print('Question 5: I want to get the weekly forecast starting the 13-08-2018. What ECMWF model run should I use to find the lead time 4 forecast?')
print('Enter the date in the format DD-MM-YYYY')
print('')

Q1answer = "23-07-2018"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again.  Remember to answer in DD-MM-YYYY.')
    Q1response = input('Your answer : ')
print('Well done. Lead Time 4 starts from three weeks before first day of the week.')

print('')
print('Question 6: I want to look at the skill of the August 2018 model. What is the earliest ECMWF model run I should use if I want to look at the skill up to a 4-week lead time?')
print('A: 02-08-2018')
print('B: 02-08-1998')
print('C: 05-07-1998')
print('D: 12-07-1998')
print('E: 12-07-2018')

print('')

Q1answer = "E"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again.  Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. The first ECMWF model run in August 2018 is 02-08-2018. The 4-week lead time is therefore 12-07-2018.')


print('Thanks ' +name + ' for playing! Best of luck for the rest of the workshop!')