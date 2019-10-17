''' Homework 7 - Sentiment Analysis

    Authors: Owen Bezick, Hermione Su
'''

from csc121.twitter import get_tweets, get_cached_tweets, pretty_print


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
        
        Parameter:
            texts - list of strings of tweets.
        
        Return:
            Score - sentiment analysis score.
    '''
    
    if affin_dict == None:
        return 0
    
    valence_score = 0
    for tweet in tweets:
        words = tweet.split()
        for word in words:
            word_lower = word.lower()
            if word_lower in affin_dict:
                valence_score += affin_dict[word_lower]
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
    
    print(text)
    #Calculate average valence score of the text. 
    score = calculate_scores(text, create_affin_dict())
    
    return score

def main():
    print(analyze_tweets('sauce'))
    
if __name__ == '__main__':
    main()
    
    