from flair.nn import Classifier
from flair.data import Sentence

classifier = Classifier.load('sentiment')
sentence = Sentence("I had heard that Holy Grail was a hilarious flick, so I was pretty excited as the opening credits rolled by. It was supposedly \"the epitome of British comedy\". If this is the best that British comedy has to offer, I think I'll stay American, thank you. The movie was absolutely stupid. Now, I like certain types of stupid comedy, but this movie just didn't cut it. It was a waste of my time. If you want to see real British comedy, check out the old game show \"Whose Line is it Anyway?\" If you want to see garbage put on film, Holy Grail is the movie for you.")
classifier.predict(sentence)
print(sentence)