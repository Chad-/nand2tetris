import sys, re
from enum import Enum

ignoreRe = re.compile(r'/.*|^\s*$')
labelRe = re.compile(r'\s*\((.+)\).*')
aCommandRe = re.compile(r'\s*@([^\s]+).*')
cCommandRe = re.compile(r'\s*(([^\s]{0,3})=)?([^\s^;]{0,3})(;([^\s]{3}))?.*')

class LineType(Enum):
    WHITESPACE = 1
    LABEL = 2
    ACOMMAND = 3
    CCOMMAND = 4

def parse(line):
    result = ignoreRe.match(line)
    if result:
        return (LineType.WHITESPACE, None, None, None)

    result = labelRe.match(line)
    if result:
        return (LineType.LABEL, result.group(1), None, None)

    result = aCommandRe.match(line)
    if result:
        return (LineType.ACOMMAND, result.group(1), None, None)
    
    result = cCommandRe.match(line)
    if result:
        return (LineType.CCOMMAND,
                result.group(2), result.group(3), result.group(5))

def firstPass(lines, symbolTable):
    address = 0

    for line in lines:
        result = parse(line)

        if result[0] == LineType.LABEL:
            symbolTable[result[1]] = address
        elif result[0] == LineType.ACOMMAND or result[0] == LineType.CCOMMAND:
            address += 1

def codeACommand(value, symbolTable):
    digit = 0

    if value.isdigit():
        digit = int(value)
    else:
        if value not in symbolTable:
            symbolTable[value] = codeACommand.symbolCounter
            codeACommand.symbolCounter += 1

        digit = symbolTable[value]

    binary = "{0:015b}".format(digit)
    return "0" + binary

codeACommand.symbolCounter = 16

def codeCCommand(dest, comp, jump, symbolTable):
    destLookup = [None, 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
    compLookup = {'0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
            'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
            '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110', 
            'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111', 
            'D&A':'0000000','D|A':'0010101', 'M':'1110000',  '!M':'1110001',
            '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010','D+M':'1000010',
            'D-M':'1010011','M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101' }
    jumpLookup = [None, 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

    i = destLookup.index(dest)
    destBinary = "{0:03b}".format(i)

    i = jumpLookup.index(jump)
    jumpBinary = "{0:03b}".format(i)
    return "111" + compLookup[comp] + destBinary + jumpBinary

def secondPass(lines, symbolTable):
    output = ""

    for line in lines:
        result = parse(line)

        if result[0] == LineType.ACOMMAND:
            output += codeACommand(result[1], symbolTable)
            output += '\n'
        elif result[0] == LineType.CCOMMAND:
            output += codeCCommand(result[1], result[2], result[3], symbolTable)
            output += '\n'

    return output

def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    file = open(inputFile)
    lines = file.readlines()
    file.close()

    symbolTable = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
            'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
            'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14,
            'R15':15, 'SCREEN': 16384, 'KBD': 24576}

    firstPass(lines, symbolTable)
    result = secondPass(lines, symbolTable)

    output = open(outputFile, "w")
    output.write(result)
    output.close()

if __name__ == "__main__":
    main()
