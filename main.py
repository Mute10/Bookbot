import string 
import requests 
from bs4 import BeautifulSoup 
#pip install requests beautifulsoup4


def commonWords(text, numOfWords=10): 
    #text (str): The input text to analyze
    #numOfWords (int, optional): Number of top words to return. Defaults to 10.
   
    text = ''.join(char.lower() for char in text if char.isalpha() or char.isspace())
    # ^ Convert text to lowercase and remove non-alphabetic characters.
   #isalpha() returns True if a character is a letter (a-z or A-Z)
   #isspace() returns True if a character is whitespace and doesn't count them and aids with text.split
    words = text.split() #Split text into individual words to avoid returning one large string
    wordCount = {} #Dictionary for word frequency counting
    exclude = { #most common words in English to exclude from the analysis.
        "the", "and", "a", "to", "of", "in", "i", "is", "that", "it",
        "for", "on", "with", "by", "at", "from", "as", "was", "were",
        "this", "are", "be", "have", "has", "had", "an", "they",
        "their", "but", "or", "not", "which", "can", "would", "may",
        "also", "these", "into", "such", "other", "than", "its", "two",
        "more", "some", "when", "may", "many", "most" 
        }
        

    for w in words: #Iterates through the entire document/web page
        if w not in exclude:
           wordCount[w] = wordCount.get(w, 0) + 1 #get current count (default 0 if word not seen) and increment by 1

    sortedWords = sorted(wordCount.items(), key=lambda x : x[1], reverse=True)
    # ^ Sort words by frequency (highest to lowest)
    # lambda x: x[1] tells sort to use the count (value) instead of the word (key)
    return sortedWords[:numOfWords] #returns top 10 used words

def webScrap(url): #Scrapes and cleans text content from a Wikipedia URL.
    #the parameter url (str): Wikipedia URL to scrape
    response = requests.get(url) # Attempt to fetch the webpage
    if response.status_code == 200: #Proceed only if the request was successful (status code 200)
        soup = BeautifulSoup(response.text, 'html.parser')  # Create BeautifulSoup object for HTML parsing
        
        for unwanted in soup(['script', 'style', 'footer', 'ref', 'cite', 'table']):
            unwanted.decompose() #Removes unwanted HTML elements that don't contain main article content
            
       # Finds the main article content div
        article = soup.find('div', {'class': 'mw-parser-output'})
        if article: # Extracts text with single spaces between words and no leading/trailing whitespace
            text = article.get_text(separator=' ', strip=True) # both text updates Normalize unordinary spaces
            text = ' '.join(text.split()) 
            return text #str: Cleaned article text or empty string if scraping fails
    return ""


def analysis(text, source): 
    #text (str): Text content to analyze
    #source (str): Description of text source (e.g. "book" or "article")
    print("\n")
    words = text.split() # Split text into words and count them
    wordCount = len(words) 
    charCounts = bookDict(text)  # # Get dictionary of character frequencies
    #print(f"{wordCount} words found in the {source}.")5510
    report(wordCount, charCounts)  # Generates and displays analysis report


def bookDict(text):
   #text (str): Input text to analyze
   charCount = {}  
   for t in text:               
       t = t.lower() # Convert to lowercase for case-insensitive counting
       if t in string.ascii_lowercase: # (must import string) Only count ASCII letters (a-z), ignore numbers/symbols
        charCount[t] = charCount.get(t, 0) + 1  #begins the letter count
   return charCount
 

def main():
    #Provides loop handling user interaction and text analysis options. Also provides options for analyzing Wikipedia links and local text files.
    wikiUrl = "https://en.wikipedia.org/wiki/Breaking_Benjamin"#reads this wikilink if field is black
    wikiContent = webScrap(wikiUrl)
    analysis(wikiContent, "Breaking Benjamin Article")

   # Reads my local Frankenstein book 
    with open("books/frankenstein.txt") as f:
        file_contents = f.read()
    result = bookDict(file_contents)

    while True: #Infinite loop until user chooses to exit
        #Menu Options below
        print("\nMain Menu:")
        print("1. Analyze Wikipedia Article") #I chose a nautilus for my first entry. 
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")
        
        if choice == "1": #what happens based on the number entered
            url = input("Enter Wikipedia URL (or press enter for a default article): ")
            if not url:
                url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
            
            try:
                content = webScrap(url)  #Attempt to scrape the webpage you entered
                print("\nArticle Content:")
                print(content) 
                #print(content[:500] + "...") Show clipped version instead of full 
                
                print("\nMost Common Words:")
                common_words = commonWords(content)  # Using your existing commonWords function
                for word, count in common_words: #forms the list and
                    print(f"'{word}' appears {count} times")   # Displays each word and its count
                    
            except Exception as e:  # Handles any errors that occur during scrapping
                print(f"An error occurred: {e}")
        
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.") # Handles invalid menu choices

    
#def sortThis(dict): # Simple helper function that returns the 'num' value for sorting
 #return dict["num"] #not needed

def report(words, charCount):
    # Creates a report of character frequencies
    charReport = []
    for char, count in charCount.items():
        if char.isalpha():  # Filters for alphabetic characters only
            charDict = {"char": char, "num": count}
            charReport.append(charDict)  # Converts the dictionary to a list of dictionaries

    charReport.sort(reverse=True, key=lambda d: d["num"]) # Sort the list of dictionaries by the 'num' field in descending order
    # charReport.sort(key=lambda d: d["char"]) #Optional: sort alphabetically

    print("--- Begin report of books/frankenstein.txt ---")
    print(f"{words} words found in the document")  # Formats the output as required
    for item in charReport:
        print(f"The '{item['char']}' character was found {item['num']} times")  # Prints characters and counts
    print("--- End report ---")


"""
alternate cleaner version of the report function:

    def report(words, charCount):
    # Filter and sort character frequencies directly
    sortedCharCount = sorted(
        ((char, count) for char, count in charCount.items() if char.isalpha()),
        key=lambda item: item[1],
        reverse=True
    )

    # Print the report
    print("--- Begin report of books/frankenstein.txt ---")
    print(f"{words} words found in the document")  # Formats the output as required
    for char, count in sortedCharCount:
        print(f"The '{char}' character was found {count} times")  # Prints characters and counts
    print("--- End report ---")
"""

def getText():
    # File handling and text processing
    with open("books/frankenstein.txt") as f: #Opens and reads the file
        textContent = f.read()
        someWords = textContent.split() #Counts words using split()
        wordCount = len(someWords)
        textDict = {} 

    for t in textContent.lower(): #Properly handles lowercase conversion
       if t not in textDict: #and begins counting
          textDict[t] = 0
       textDict[t] += 1
    return wordCount, textDict #never try to unpack single value into two variables
wordCount, countChars = getText() #both variables call the function
report(wordCount, countChars)

def counter():
 count = 0
 with open("books/frankenstein.txt") as f: #Opens and begins processing the local txt file
  content = f.read().split() # Read the file and split the content into words based on whitespace
  count = len(content) # Get the total number of words in the file
  print(count) 

  #the purpose of the code below is to learn how append and write work
 with open("books/my_story.txt", "w") as new_file:  # Changed "a" to "w" as "a"  it increments the text + 1. Using “w” starts fresh each time.
        #Open (or creates) "my_story.txt" in write mode to start fresh
        new_file.write("Cloud defeats Sephiroth with his buster sword and with some help from Tifa.\n" 
             "Cloud and Tifa vanish without a trace shortly after. \n")
        
 with open("books/my_story.txt", "r") as honey: #"my_story.txt" in read mode
        honey_story = honey.read()
        print(honey_story) 
 
 return count #Return the word count from "frankenstein.txt"

#counter() #execute the above operations

# This final block is a common Python idiom to ensure this script runs correctly if executed directly
if __name__ == "__main__":
 counter()
 main()

 #Final synopsis:  Consider performance improvements, but only if your dataset grows too large.
