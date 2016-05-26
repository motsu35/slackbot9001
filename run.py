from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import random
import re
import sys

def main():
    markov_file = open(sys.argv[1])
    global markov_obj
    markov_obj = Markov(markov_file)
    bot = Bot()
    bot.run()

@listen_to('\\btom\\b', re.IGNORECASE)
def tom(message):
    global markov_obj
    #message.reply(filter(lambda x: x in string.printable, markov_obj.generate_markov_text()))
    message.reply(markov_obj.generate_markov_text())
    message.react('thetom')

@listen_to('\\bfoundation\\b', re.IGNORECASE)
def foundation(message):
    global markov_obj
    message.reply(markov_obj.generate_markov_text())
#    message.react('thetom')

@respond_to('I love you')
def love(message):
    message.reply('I love you too!')

@respond_to('money')
def money(message):
    message.reply('YES! i love da money! $$$$ :moneybag:')


#markov shit
class Markov(object):
    
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()
        
    
    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words
        
    
    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """
        
        if len(self.words) < 3:
            return
        
        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])
            
    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]
                
    def generate_markov_text(self, size=10):
        seed = random.randint(0, self.word_size-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        i = 0
        gen_words.append(w1)
        #skip to next sentence to avoid fragmented beginnings.
        while (not (gen_words[len(gen_words)-1].endswith("."))):
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
                gen_words.append(w1)
        #now clear for the next bit.
        del gen_words[:]
        w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w1)
        #now build the thing for real.
        while (not (gen_words[len(gen_words)-1].endswith("."))) or i < size:
            if (w1, w2) in self.cache:
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
                gen_words.append(w1)
                i += 1
            else:
                print "shit..."
                possible_next_word = []
                for i in xrange(len(self.words)):
                    if unicode(w1.lower()) == unicode(self.words[i].lower()):
                        possible_next_word.append(i)
                w2 = self.words[random.choice(possible_next_word)+1]
                gen_words.append(w1)
                i += 1
        
        if(sum(len(letters) for letters in gen_words) < 300):
            return ' '.join(gen_words)
        else:
            return self.generate_markov_text()
    
    def generate_markov_text_with_seed(self, seed, size=10):
        #get list of seed index's
        seed_index_list = []
        for i in xrange(len(self.words)):
            if unicode(seed.lower()) == unicode(self.words[i].lower()):
                seed_index_list.append(i)

        seed_word, next_word = self.words[random.choice(seed_index_list)] , self.words[random.choice(seed_index_list)+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        i = 0
        gen_words.append(w1)
        while (not (gen_words[len(gen_words)-1].endswith("."))) or i < size:
            if (w1, w2) in self.cache:
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
                gen_words.append(w1)
                i += 1
            else:
                print "shit..."
                possible_next_word = []
                for i in xrange(len(self.words)):
                    if unicode(w1.lower()) == unicode(self.words[i].lower()):
                        possible_next_word.append(i)
                w2 = self.words[random.choice(possible_next_word)+1]
                gen_words.append(w1)
                i += 1

        if(sum(len(letters) for letters in gen_words) < 300):
            return ' '.join(gen_words)
        else:
            return self.generate_markov_text_with_seed(seed)







if __name__ == "__main__":
    main()
