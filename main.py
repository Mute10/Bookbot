import string

def bookDict(text):#the purpose of this function it to count how any letters are in a file
   charCount = {}  # if a letter doesn't exist i won't print anything
  #charCount = {ch: 0 for ch in string.ascii_lowercase} this targets every letter from a - z
   for t in text:
       t = t.lower() 
       if t not in charCount:
        charCount[t] = 0 #if you remove this all letters become zero
       charCount[t] += 1 #calling charCount by itself will turn everything to 0(, . and spaces)
   return charCount
 

def main():
    with open("books/frankenstein.txt") as f:
        file_contents = f.read() #this file contains 77968 words
    #print(file_contents)
    result = bookDict(file_contents)
    print(result)
    print("\n")

if __name__ == "__main__":
    main()

def sortThis(dict): #Provides the sorting key for the character counts
 return dict["num"]

def report(words, charCount):
   charReport = []
   for char, count in charCount.items():
      if char.isalpha(): #Filters for alphabetic characters using isalpha()
         charDict = {"char": char, "num": count}
         charReport.append(charDict) #Converts the dictionary to a list of dictionaries
   charReport.sort(reverse=True, key=sortThis) #reverse = descending order
   #charReport.sort(key=lambda d: d["char"]) sorts alphabetically
   print("--- Begin report of books/frankenstein.txt ---")
   print(f"{words} words found in the document") #Formats the output exactly as required
   for item in charReport:
      print(f"The '{item['char']}' character was found {item['num']} times")
   print("--- End report ---")


def getText():
    with open("books/frankenstein.txt") as f: #Opens and reads the file
        textContent = f.read()
        someWords = textContent.split() #Counts words using split()
        wordCount = len(someWords)
        textDict = {} #Creates a dictionary to count characters
    for t in textContent.lower(): #Properly handles lowercase conversion
       if t not in textDict:
          textDict[t] = 0
       textDict[t] += 1
    return wordCount, textDict #never try to unpack single value into two variables
wordCount, countChars = getText()
report(wordCount, countChars)

def counter():
 count = 0
 with open("books/frankenstein.txt") as f: #You open the file
  content = f.read().split() #Read and split f into words. the f is like a variable
  count = len(content) # counts all the words
  print(count) 

 with open("books/my_story.txt", "w") as new_file:  # Changed "a" to "w" as "a"  it increments the text + 1. Using “w” starts fresh each time.
        new_file.write("The wizard bear practiced his magic spells. His honey pot never seemed to run dry.\n" 
             "The honey goblins have been unable to steal any for a few months now. \n")
             #the purpose of my story.txt is to learn how append and write work
 with open("books/my_story.txt", "r") as honey:
        honey_story = honey.read()
        print(honey_story)
 
 return count


counter()