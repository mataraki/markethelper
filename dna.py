import csv
import sys

def main():
    
    # Ensure correct usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py DATABASE SEQUENCE")
        sys.exit()
    
    dnas = []
    
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dna = {}
            dna = row
            dna = integerize(dna)
            dnas.append(dna)
            
    with open(sys.argv[2], "r") as file:
        sequence = file.read()
            
    for dna in dnas:
        if "AGATC" in dna:
            if dna["AGATC"] != STRfinder(sequence, "AGATC"):
                continue
        if "TTTTTTCT" in dna:
            if dna["TTTTTTCT"] != STRfinder(sequence, "TTTTTTCT"):
                continue
        if "AATG" in dna:
            if dna["AATG"] != STRfinder(sequence, "AATG"):
                continue
        if "TCTAG" in dna:
            if dna["TCTAG"] != STRfinder(sequence, "TCTAG"):
                continue
        if "GATA" in dna:
            if dna["GATA"] != STRfinder(sequence, "GATA"):
                continue
        if "TATC" in dna:
            if dna["TATC"] != STRfinder(sequence, "TATC"):
                continue
        if "GAAA" in dna:
            if dna["GAAA"] != STRfinder(sequence, "GAAA"):
                continue
        if "TCTG" in dna:
            if dna["TCTG"] != STRfinder(sequence, "TCTG"):
                continue
        print(dna["name"])


def STRfinder(sequence, STR):
    count = 0
    temp = STR

    while sequence.find(temp) != -1:
        count += 1
        temp += STR
        
    return count

    
def integerize(dna):
    for i in range(len(dna)):
                if "AGATC" in dna:
                    dna["AGATC"] = int(dna["AGATC"])
                if "TTTTTTCT" in dna:
                    dna["TTTTTTCT"] = int(dna["TTTTTTCT"])
                if "AATG" in dna:
                    dna["AATG"] = int(dna["AATG"])
                if "TCTAG" in dna:
                    dna["TCTAG"] = int(dna["TCTAG"])
                if "GATA" in dna:
                    dna["GATA"] = int(dna["GATA"])
                if "TATC" in dna:
                    dna["TATC"] = int(dna["TATC"])
                if "GAAA" in dna:
                    dna["GAAA"] = int(dna["GAAA"])
                if "TCTG" in dna:
                    dna["TCTG"] = int(dna["TCTG"])
                    
    return dna
        
        
if __name__ == "__main__":
    main()
