from cs50 import get_int

number = get_int("Number: ")
number2 = number
length = 2
    
while True:
    number2 = int(number2 / 10)
    length = length + 1
    if number2 < 100:
        break
    
luhn = 0
i = 1
    
while True:
    if i % 2 == 1:
        luhn += number % 10
        number = int(number / 10)
        
    else:
        luhn += int(((number % 10) * 2) / 10)
        luhn += ((number % 10) * 2) % 10
        number = int(number / 10)
        
    i += 1
    
    if number == 0:
        break
    
if luhn % 10 == 0:
    if (number2 == 34 or number2 == 37) and (length == 15):
        print("AMEX")
        
    elif (number2 > 50 and number2 < 56) and (length == 16):
        print("MASTERCARD")
        
    elif (number2 / 10 == 4) and (length == 13 or length == 16):
        print("VISA")
        
    else:
        print("INVALID")
    
else:
    print("INVALID")