#!/usr/bin/env python
# coding: utf-8

# In[1]:

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import praw
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resultPath = os.path.join(BASE_DIR, 'analytics','result.png')

# In[2]:


reddit = praw.Reddit(client_id='S7Ij8TubFtWdgw',
                     client_secret='fsLH6NrVsONjSeP42TrCDwIB4b4',
                     redirect_uri='http://localhost:8080',
                     user_agent='testscript by /u/LankyDescription')


# In[3]:


subreddit = reddit.subreddit("uwaterloo")


# In[10]:


top_subreddit = subreddit.top(limit=10)


# In[11]:


#for submission in top_subreddit:
#    print(submission.selftext)


# In[38]:


# remove punctuation
def removePunctuation(word):
    punctuation = ['!', '?', '-', ',', '.', "'", '"']
    for char in punctuation:
        if char in word:
            word.replace(char, "")
    return word

# add 's' suffix
def combinePlural(dictionary, word):
    if word + 's' in dictionary:
        word += dictionary[word + 's']
    

# main function
def plotGraph(subredditName, keyword):
    
    # initialize subreddit according to parameter
    subreddit = reddit.subreddit(subredditName)
    
    # get last 900 submissions from subreddit
    latest = subreddit.new(limit=900)
    
    # initialize empty list to keep dictionary of words for each interval
    wordList = [{}]
    
    # initialize x-axis and y-axis intervals and submission count
    submissionCount = 0
    i = 0
    x = range(100, 901, 100)
    y = []
    
    # iterate through submissions and keep count of every word in description
    for submission in latest:
        
        submissionCount += 1
    
    # document words from title
        for word in submission.title.lower().split():
            if removePunctuation(word) in wordList[i]:
                wordList[i][word] += 1
            else:
                wordList[i][word] = 1
    
    # document words from description
        for word in submission.selftext.lower().split():
            if removePunctuation(word) in wordList[i]:
                wordList[i][word] += 1
            else:
                wordList[i][word] = 1
                
    # determine if loop has reached an interval and should start a new dictionary
        if submissionCount == x[i]:
            if keyword in wordList[i]:
                y.append(wordList[i][keyword])
                
    # take into account the plural form of the keyword
                if keyword + 's' in wordList[i]:
                    wordList[i][keyword] += wordList[i][keyword + 's']
                
            else:
                y.append(0)
            i += 1
            wordList.append({})
    
    
    # plot a graph
    plt.plot(x, y[::-1], label = keyword)
    plt.xlabel("oldest to newest")
    plt.ylabel("frequency")
    plt.title("trend for " + "/r/uwaterloo")
    plt.legend() 
    plt.savefig(resultPath, bbox_inches='tight') 


# In[ ]:




