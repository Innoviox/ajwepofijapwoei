import sys

EXECUTION_LIMIT = 1000000
SIZE_LIMIT = 250
STACK_LIMIT = 10000
from math import sqrt
def F(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))
trialInputs = [["221\n-2\n3\n0\n"]]
trialOutputs = ['1', '1', '2', '3', '5', '8', '13', '21', '34', '55', '89', '144', '233', '377', '610', '987', '1597', '2584', '4181', '6765', '10946', '17711', '28657', '46368', '75025', '121393', '196418', '317811', '514229', '832040', '1346269', '2178309', '3524578', '5702887', '9227465', '14930352', '24157817', '39088169', '63245986', '102334155', '165580141', '267914296', '433494437', '701408733', '1134903170', '1836311903']
print(trialOutputs)

FLAG = "omitted"

ppcct = open('ppcct.dat', 'r', encoding = "ISO-8859-1").read()

class Position:
        def __init__(self):
                self.pos = (0, 0)
                self.dir = (1, 0)

        def getLocation(self):
                return self.pos

        def setLocation(self, newPos):
                self.pos = newPos
                self.fix()

        def fix(self):
                self.pos = ((self.pos[0] + SIZE_LIMIT) % SIZE_LIMIT, (self.pos[1] + SIZE_LIMIT) % SIZE_LIMIT)

        def previous(self):
                self.pos = (self.pos[0] - self.dir[0], self.pos[1] - self.dir[1])
                self.fix()

        def next(self):
                self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
                self.fix()

        def changeDirection(self, c):
                if c == '_':
                        self.dir = (self.dir[0], -self.dir[1])
                if c == '|':
                        self.dir = (-self.dir[0], self.dir[1])

                if c == '/':
                        self.dir = (-self.dir[1], -self.dir[0])

                if c == '\\':
                        self.dir = (self.dir[1], self.dir[0])

                return True

class PingPongStack:
        def __init__(self):
                self.data = []

        def push(self, i):
                if len(self.data) < STACK_LIMIT - 1:
                        self.data.append(abs(i) % (2**32) * (1 if i > 0 else -1))
                        return True
                return False

        def pop(self):
                return 0 if len(self.data) == 0 else self.data.pop()

        def peek(self):
                return 0 if len(self.data) == 0 else self.data[-1]

        def add(self):
                return self.push(self.pop() + self.pop())

        def subtract(self):
                a = self.pop()
                return self.push(self.pop() - a)

        def multiply(self):
                return self.push(self.pop() * self.pop())

        def divide(self):
                divisor = self.pop()
                dividend = self.pop()
                self.push(0 if divisor == 0 else dividend // divisor)
                return self.push(0 if divisor == 0 else dividend % divisor)

        def andOperator(self):
                return self.push(self.pop() & self.pop())

        def complement(self):
                return self.push(~self.pop())
                return True

        def remove(self):
                self.pop()
                return True

        def duplicate(self):
                a = self.pop()
                self.push(a)
                return self.push(a)

        def switch(self):
                a = self.pop()
                b = self.pop()
                self.push(a)
                self.push(b)
                return True

        def moveOver(self, other):
                return other.push(self.pop())

        def moveBack(self, other):
                return self.push(other.pop())

        def checkCondition(self, c):
                top = self.peek()
                return ((c == '=') & (top == 0)) | ((c == '>') & (top > 0)) | ((c == '<') & (top < 0))

        def getPointer(self):
                self.pop()
                x = self.pop()
                y = self.pop()
                return [x, y]

        def addPointer(self, loc):
                self.push(loc[1])
                self.push(loc[0])
                return self.push(0)

        def addString(self, s):
                good = True
                self.push(-1)
                for i in s[::-1]:
                        good = good & self.push(ppcct.index(i))
                return good

        def addInteger(self, s):
                intS = 0
                try:
                        intS = int(s)
                except ValueError:
                        print("Read wrong type of input.")
                        sys.exit()
                return self.push(intS)

def getCodepoint(cod, locat):
        if locat in code:
                return cod[locat]
        return " "

print("Enter your PP code, line by line, or paste it all in at once. Enter an empty line when you are done ==>")
inputList = []
string = input()
while string != "":
        if len(string) > SIZE_LIMIT or len(inputList) >= SIZE_LIMIT:
                print("Code too large, aborting.")
                sys.exit()
        inputList.append(string)
        string = input()

code = {}
for i in range(0, len(inputList)):
        for j in range(0, len(inputList[i])):
                c = inputList[i][j]
                if ppcct.index(c) == -1:
                        print("Encountered invalid character.")
                        sys.exit()
                code[(j, i)] = inputList[i][j]

for i in range(0, len(trialInputs)):
        a=0
        p = Position()
        s = PingPongStack()
        hs = PingPongStack()

        cc = 0

        inp = trialInputs[i]
        inputCount = 0
        outpt = trialOutputs[i]
        actualOut = ""

        forcePush = False
        bounds = True

        com = getCodepoint(code, p.getLocation())
        while com != "@":
                a += 1
                #print(a)
                print(str(p.getLocation()) + ", " + com + ": " + str(s.data) + str(hs.data))
                out = True
                if forcePush:
                        out = s.push(ppcct.index(com))
                        forcePush = False
                elif com == "$":
                        forcePush = True
                elif com == "+":
                        out = s.add()
                elif com == "-":
                        out = s.subtract()
                elif com == "*":
                        out = s.multiply()
                elif com == "%":
                        out = s.divide()
                elif com == "&":
                        out = s.andOperator()
                elif com == "~":
                        out = s.complement()
                elif com == "!":
                        out = s.remove()
                elif com == "\"":
                        out = s.duplicate()
                elif com == "^":
                        out = s.switch()
                elif com == "`":
                        out = s.moveOver(hs)
                elif com == "'":
                        out = s.moveBack(hs)
                elif com == ",":
                        if len(inp) > inputCount:
                                out = s.addString(inp[inputCount])
                                inputCount += 1
                        else:
                                out = False
                elif com == ";":
                        if len(inp) > inputCount:
                                out = s.addInteger(inp[inputCount])
                                inputCount += 1
                        else:
                                out = False
                elif com == ".":
                        #print(str(p.getLocation()) + ", " + com + ": " + str(s.data) + str(hs.data))
                        actualOut = actualOut + ppcct[abs(s.pop()) % 256]
                elif com == ":":
                        string = str(s.pop())
                        actualOut += string
                elif com == ">" or com == "<" or com == "=":
                        if s.checkCondition(com):
                                p.next()
                elif com == "#":
                        p.next()
                elif ((com == "\\") or (com == "/") or (com == "_") or (com == "|")):
                        p.changeDirection(com)
                elif com == " " or com == "D" or com == "d":
                        pass
                elif com == "[":
                        oldLoc = p.getLocation()
                        p.setLocation(s.getPointer())
                        com = s.addPointer(oldLoc)
                        p.previous()
                elif com == "]":
                        p.setLocation(s.getPointer())
                else:
                        out = s.push(ppcct.index(com))

                cc += 1
                if not out:
                        print("Exceeded bounds or took too much input.")
                        sys.exit()
                if cc > EXECUTION_LIMIT:
                        print("Exceeded bounds or took too much input.")
                        sys.exit()

                p.next()
                com = getCodepoint(code, p.getLocation())
                #input()
        print(actualOut + ", " + outpt)
        if actualOut != outpt:
                print("Incorrect.")
                sys.exit()

print("Correct! The flag is " + FLAG + ".")
sys.exit()

'''
;1-=\1.@
    \1-11``#/         =\!''!0^#/        =\!#/   =\@
            \-1`+^`"^''/       \`%*25'+1`/  \-1.'/
'''

''' 
,#/  #/#/ #/          #/      1+=\@
                       \!/=-*N6-1/
           \!.*N6.'/=+*N6/
        \  [0*685/>/
      \            /
]0+1*523!'!/=-*6N  \#\#  \# `!/=  \#\#\#'-10`!!!
           \6N*+=\!/          \'=\/
                                 \^ /
                 \`  /

,#/#/                   #/            #/            1+=\800]            
                                                       \1-585*1+*-\
                                       \`!*N6`*-10!/=             /
                         \`!+*N6'^`/= -*N6`+*+1*585/
                       [008/=+1+*6N/
    \`+*N6/=     -*N6`\#'-1/
          \6N*+'52**+ /                 
#/=\@
 \'/
 
/6N*+'52**+\                                          


                  \=\!01-*
                    \585*1+*+`6N*-=\`^'
                                   \6N*+'#/`6N*-    =\
                                          \+**25'+*N6/




9m



            
/=+1         \#\#  \#
         \=\!/
           \`  \
]0+1*523 !!/=`!/= \#'-10`!!!
]0+1*523 !`/   \'^/

'''
