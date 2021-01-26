from flask import Flask, jsonify
import operator


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# LOGIC
def getWords(letters, filePath):
    possible_words = []
    file = open(filePath, "r")
    for line in file:
        if line[0] == letters[0]:
            line = line.strip("\n")
            line = line.replace("\n", '')
            line_ = list(line)
            letters_ = list(letters)
            #print(line_, letters_)
            for letter in list(line):
                if letter in list(letters):
                    if line_.count(letter) > letters_.count(letter):
                        break
                    #print(letter)
                    line_.remove(letter)
                    letters_.remove(letter)
            if len(line_) == 0:
                possible_words.append(line)
    return possible_words

def getPoints(word):
    letter_values = {'a':1 , 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}
    points = 0
    for letter in word:
        points += letter_values[letter]
    return points

@app.route('/')
def home():
    return "Main API home page, built by Dhanush Eashwar. Use scrabble-api.herokuapp.com/api/<your letters>"

@app.route('/api/<letters>', methods=["GET"])
def api(letters):
    my_words = {
        "Options": {},
    }
    for word in getWords(letters, "words.txt"):
        my_words["Options"][word] = getPoints(word)
    my_words_options = sorted(my_words["Options"].items(),key=operator.itemgetter(1),reverse=True)
    my_words["Options"] = dict(my_words_options)
    best_word = max(my_words["Options"], key=my_words["Options"].get)
    my_words["Best Word"] = {best_word: getPoints(best_word)}
    return jsonify(my_words)

if __name__ == "__main__":
    app.run()
