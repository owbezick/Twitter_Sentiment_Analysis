''' Homework 7 Extra Credit

    Sentiment Analysis that includes Emojis and strips punctuation.

    Author: Owen Bezick
'''

from csc121.twitter import get_tweets, get_cached_tweets, pretty_print
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import emoji
import string

def get_text(tweets):
    '''
        Isolates textual data from tweets.

        Parameters:
                Tweets - Tweet query.
        Returns:
                Text - list of strings containing
                the contents of tweet query.
    '''
    
    text = []
    list_of_dictionaries = tweets["statuses"]
    for i in range(len(list_of_dictionaries)):
        dictionary_i = list_of_dictionaries[i]
        text.append(dictionary_i["text"])
    return text


def strip_emoji_and_punctuation(text):
    '''
        Replaces emojis with their textual equivalent and strips the
        text of punctuation.
        
        I used the emoji package to replace emojis with their textual
        equivalents. For instance, ❤ will be :red_heart:, and after the underscore
        and punctuation is removed it will just be red heart. Then, the corresponding
        text will be evaulated using Finn Nielson's dictionary.
        
        A problem with this sort of analysis is that 'heart' is not located within the
        dictionary. A red heart would mean some sort of sentiment, say a positive 3 or 4,
        but using this dictionary as a tool of evaluation renders it a 0.
        
        Parameters:
            text
            
        Returns:
            text_wo_emoji_and_punctuation 
    '''
    #Emoji
    text_wo_emoji = []
    for i in text:
        text_wo_emoji.append(emoji.demojize(i).replace("_"," "))

    #Punctuation
    translator = str.maketrans('', '', string.punctuation)
    text_wo_emoji_and_punctuation = []
    for i in text_wo_emoji:
       text_wo_emoji_and_punctuation.append(i.translate(translator))
    return text_wo_emoji_and_punctuation
    
    
def create_affin_dict():
    '''
        Creates a dictionary of words as keys and their
        scores as values.
        
        Parameters:
                None
        
        Returns:
                affin_dict - dictionary of words and values.
    '''
    
    try:    
        affin_dict = {}
        with open("AFINN-111.txt", "r") as in_file:
            for line in in_file:
                word = line.split()
                affin_dict[word[0]] = int(word[1])
            return affin_dict
    except:
        print("Error when reading file.")
        
        
def calculate_scores(tweets, affin_dict):
    '''
        Calculate the score of the texts.
        
        Text is transfered to lower case, so it it can be evaluated
        using the dictionary. Also, each word is changed to its stem
        so that emojis such as "smiling face' will be evaluated as
        'smile face' to increase its chances of being located in the
        dictionary.
        
        Parameter:
            texts - list of strings of tweets.
        
        Return:
            Score - sentiment analysis score.
    '''
    if affin_dict == None:
        return 0
    
    ps = PorterStemmer()
    
    valence_score = 0
    for tweet in tweets:
        words = tweet.split()
        for word in words:
            word_lower = word.lower()
            stem = ps.stem(word_lower)
            if stem in affin_dict:
                valence_score += affin_dict[stem]
            else:
                valence_score += 0
            
    if len(tweets) > 0:
        score = valence_score / len(tweets)
    else:
        return 0
    
    return score


def analyze_tweets(query_term):
    '''
        Uses the supplied query term to retrieve tweets in
        real-time from Twitter and returns the sentiment score of
        the set of tweets.
        
        Valence scores for each word are retrieved from Ffin Nielson's
        evaluation.
        
        Parameters:
                query_term - term to be queried
        
        Return:
                score - sentiment score
    '''
    
    #Get tweets with the query term.
    tweets = get_tweets(query_term)
    
    #Isolate text of tweets.
    text = get_text(tweets)
    
    #Strip emojis and texts.
    final_text = strip_emoji_and_punctuation(text)
    
    #Calculate average valence score of the text. 
    score = calculate_scores(final_text, create_affin_dict())
    
    return score

def main():
    print(strip_emoji_and_punctuation(['! ❤️']))
    
if __name__ == '__main__':
    main()
    
    