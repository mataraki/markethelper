from cs50 import get_string

def main():
    text = get_string("Text: ")
    grade = int(getgrade(text))
    
    if grade < 1:
        print("Before Grade 1")
    
    elif grade > 16:
        print("Grade 16+")
    
    else:
        print(f"Grade {grade}")
    
def getgrade(text):
    letters = 0
    words = 1
    sentences = 0
    
    for i in range(len(text)):
        
        if (text[i] == '.') and (text[i - 1] != '.'):
            sentences += 1
        
        elif text[i] == '!':
            sentences += 1
        
        elif text[i] == '?':
            sentences += 1
        
        elif text[i] == ' ':
            words += 1
        
        elif (text[i] >= 'A' and text[i] <= 'Z') or (text[i] >= 'a' and text[i] <= 'z'):
            letters += 1
            
    grade = 0.0588 * letters * 100 / words - 0.296 * sentences * 100 / words - 15.8
    return grade

if __name__ == "__main__":
    main()