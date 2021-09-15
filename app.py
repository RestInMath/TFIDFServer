from flask import Flask, jsonify, request, render_template

HOME_PAGE = "index.html"
FILE_FORM = "text_file"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def get_tfidf_dict(texts):
    dict_tf = {
        #term: the frequency of term
    }
    dict_idf = {
        #term: set of ids of texts containing a term
    }

    for text_id in range(len(texts)):
        text_words = texts[text_id].split()
        for word in text_words:
            
            word = ''.join(filter(str.isalpha, word)).lower()
            if word == '':
                continue

            if word in dict_tf.keys():
                dict_tf[word] += 1
                dict_idf[word].add(text_id)

            else:
                dict_tf[word] = 1
                dict_idf[word] = {text_id}

    #combine dicts, count idf
    dict_tfidf = {}
    for word in dict_tf.keys():
        dict_tfidf[word] = [dict_tf[word], len(dict_idf[word])]

    return dict_tfidf

def sort_tfidf_dict(tfidf_dict):
    #sort by alphabet
    tfidf_dict = dict(sorted(tfidf_dict.items(), key=lambda x: x[0]))

    #then reverse sort by idf and tf
    tfidf_dict = dict(sorted(tfidf_dict.items(), \
        key=lambda x: (x[1][1], x[1][0]), reverse=True))

    return tfidf_dict

#Home page
@app.route("/")
def home():
    return render_template(HOME_PAGE)

#Get text from file
@app.route("/", methods=['POST'])
def home_post():
    
    if FILE_FORM in request.files:

        files = []
        for file in request.files.getlist(FILE_FORM):
            files.append(file.read().decode("utf-8"))

        words_stat = get_tfidf_dict(files)
        words_stat = sort_tfidf_dict(words_stat)

        #slice first 50 terms
        words_stat = dict(list(words_stat.items())[:50])

    return render_template(HOME_PAGE, data=words_stat)


#An error-handler to ensure that errors are returned as JSON
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)