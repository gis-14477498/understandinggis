# create a variable that holds a list of three words
words = ['First', 'Second', 'Third']
words.append('Fourth')
# print each of those words in turn
print(words[0])
for word in words:
# everything in the indented block is run for each of the 3 elements in the list
 print(word)
range(10)
print(list(range(10)))
range(3)
for i in range(3):
    print(i,words[i])
    
numbers = [1,2,3,4,5,6,7,8,9,10,15,30]
total = 0
for o in numbers:
    total += o
print(total)
    