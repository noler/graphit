#Ask user for input
expression = raw_input("Please, our dear paying customer enter your awsome command: ")
print "Raw input :" + expression

if '+' in expression:
    #B Specifies what to remove from string
    b = "+"

    expression = expression.replace(b, " ")
    print "New expression: " + expression

    print int(expression)

    expression = expression.split(' ')


'''
    arr = [int(num) for num in expression]


    print "Array :" + expression

    print "expression[0]: " + expression[0]
    print "expression[1]: " + expression[1]
    #print "expression[2]: " + expression[2]

    print (expression[0])+(expression[1])
'''
