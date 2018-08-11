'''
Quiz
'''

print('Welcome to the S2S data structure quiz')
name = input('What is your name?')
print('Hi there '+ name + "! Let's play a game!")
print('I will ask you 7 questions. Mix of Multiple choice and enter yourself')
print('Please keep caps lock on so all answers can be printed in caps')
print('All dates must be in the format DD-MM-YYYY')
print('-----------------------------------------------------------------')
score = 0.0


print('Question 1: What is the first ECMWF December model run in December 2017?')
print('A: 01-12-2017')
print('B: 03-12-2017')
print('C: 04-12-2017')
print('')

Q1answer = "C"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again. Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. ECMWF S2S forecasts are produced on Mondays and Thursdays. The first Monday or Thursday in December 2017 was 03-12-2017')

print('')
print('Question 2: What is the first ECMWF model run in August 2018?')
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
print('Question 5: What does hdate refer to?')
print('A: The model run date')
print('B: The reforecast date')
print('C: The lead time')

print('')

Q1answer = "B"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again.  Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. Hdate refers to the hindcast date or reforecast date.')

print('')
print('Question 6: TRMM data is available for 1998-May 2015. ECMWF forecast data is available from 2015, and ECMWF reforecast data is avaiable from 1995-2017. What years should we study if we want to assess the skill of the reforecast data using TRMM?')
print('A: 1995-2015')
print('B: 1995-2017')
print('C: 1998-2014')
print('D: 2015-')

print('')

Q1answer = "C"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again.  Remember to answer in CAPITALS.')
    Q1response = input('Your answer : ')
print('Well done. The years 1998-2014 are the only complete years when both the ECMWF reforecast and TRMM data are available.')

print('')
print('Question 7: How many ensemble members does the ECMWF reforecast data have?')


print('')

Q1answer = "11"
Q1response = input('Your answer : ')

while (Q1response != Q1answer):
    print('Sorry, that is incorrect. Try again.  Remember to answer in numerals only (e.g. "1").')
    Q1response = input('Your answer : ')
print('Well done. There are 10 perterbed reforecasts plus one control forecast (total = 11).')




print('Thanks ' +name + ' for playing! Best of luck for the rest of the workshop!')