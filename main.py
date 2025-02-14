import string
import requests
from bs4 import BeautifulSoup

#below you'll see examples of Web scraping with error handling, Text analysis (word count and character frequency),
#File handling and Multiple data sources (web and text file)
#polished off with a command-line interface where users can input their own Wikipedia URLs to analyze


def commonWords(text, numOfWords=10): 
    # Remove punctuation and clean text
    #Analyzes text for most frequent words, excluding common stop words.
    #Args: text (str): Text to analyze
    #numOfWords (int): Number of top words to return (default: 10)
    #Returns: list: Tuples of (word, count) sorted by frequency
    text = ''.join(char.lower() for char in text if char.isalnum() or char.isspace())
    words = text.split()
    wordCount = {}
    exclude = {
        "the", "and", "a", "to", "of", "in", "i", "is", "that", "it",
        "for", "on", "with", "by", "at", "from", "as", "was", "were",
        "this", "are", "be", "have", "has", "had", "an", "they",
        "their", "but", "or", "not", "which", "can", "would", "may",
        "also", "these", "into", "such", "other", "than", "its", "two",
        "more", "some", "when", "may", "many", "most" 
        }
        

    for w in words:
        if w not in exclude:
           wordCount[w] = wordCount.get(w, 0) + 1 

    sortedWords = sorted(wordCount.items(), key=lambda x : x[1], reverse=True)
    return sortedWords[:numOfWords]

def webScrap(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # First, remove the unwanted sections
        for unwanted in soup(['script', 'style', 'footer', 'ref', 'cite', 'table']):
            unwanted.decompose()
            
        # Find the main article content div
        article = soup.find('div', {'class': 'mw-parser-output'})
        if article:
            # Get all text within the article
            text = article.get_text(separator=' ', strip=True)
            # Clean up whitespace
            text = ' '.join(text.split())
            return text
    return ""


def analysis(text, source): #Performs text analysis on the scraped content.
    #print(text) #Prints the original text, word count, and character frequency analysis
    print("\n")
    words = text.split()
    wordCount = len(words)
    charCounts = bookDict(text)
    #print(f"{wordCount} words found in the {source}.")5510
    report(wordCount, charCounts)


def bookDict(text):#the purpose of this function it to count how any letters are in a file
   charCount = {}  # if a letter doesn't exist it won't print anything
   for t in text:               
       t = t.lower() 
       if t in string.ascii_lowercase: #import string or won't work
        charCount[t] = charCount.get(t, 0) + 1 #calling charCount by itself will turn everything to 0(, . and spaces)
   return charCount
 

def main(): #main menu loop for user interaction
    #wiki analysis, Accepts any valid Wikipedia URL 
    wikiUrl = "https://en.wikipedia.org/wiki/Breaking_Benjamin"
    wikiContent = webScrap(wikiUrl)
    analysis(wikiContent, "Breaking Benjamin Article")

    #book analysis
    with open("books/frankenstein.txt") as f:
        file_contents = f.read()

    result = bookDict(file_contents)

    while True:
        print("\nMain Menu:")
        print("1. Analyze Wikipedia Article") #I chose a nautilus for my first entry. 
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            url = input("Enter Wikipedia URL (or press enter for a default article): ")
            if not url:
                url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
            
            try:
                content = webScrap(url)  # Using your existing webScrap function
                print("\nArticle Content:")
                print(content) 
                #print(content[:500] + "...") a good way to shorten boring articles while indicating there's more(...)
                
                print("\nMost Common Words:")
                common_words = commonWords(content)  # Using your existing commonWords function
                for word, count in common_words:
                    print(f"'{word}' appears {count} times")
                    
            except Exception as e:
                print(f"An error occurred: {e}")
        
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    
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
   #print("--- Begin report of books/frankenstein.txt ---")
   #print(f"{words} words found in the document") #Formats the output exactly as required
   #for item in charReport:
      #print(f"The '{item['char']}' character was found {item['num']} times") #prints the letter and how many times it's used.
   #print("--- End report ---")


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
wordCount, countChars = getText() #both variables call the function
report(wordCount, countChars)

def counter():
 count = 0
 with open("books/frankenstein.txt") as f: #You open the file
  content = f.read().split() #Read and split f into words. the f is like a variable
  count = len(content) # counts all the words
  print(count) 

 with open("books/my_story.txt", "w") as new_file:  # Changed "a" to "w" as "a"  it increments the text + 1. Using “w” starts fresh each time.
        new_file.write("Cloud defeats Sephiroth with his buster sword and with some help from Tifa.\n" 
             "Cloud and Tifa vanish without a trace shortly after. \n")
             #the purpose of my story.txt is to learn how append and write work
 with open("books/my_story.txt", "r") as honey:
        honey_story = honey.read()
        #print(honey_story) 
 
 return count


counter()

if __name__ == "__main__":
 main()

