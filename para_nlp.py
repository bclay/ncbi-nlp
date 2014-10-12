# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
#imports
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


# configuration
DATABASE = '/tmp/ncbi_nlp.db'
#next two lines are lazy and inappropriate for deployment
DEBUG = True
SECRET_KEY = 'complexity'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#create an array of tokens
#input: string
#output: array of tokens (words)
def create_tokens(str):
	tokenizer = RegexpTokenizer(r"\w+(-\w+)*")
	words = tokenizer.tokenize(str)
	lc_words = [w.lower() for w in words]
	return lc_words

#remove stop words
#input: a large token array representing multiple summaries
#output: dictionary with words counts
def rm_words(word_arr):
	d = {}
	stop = stopwords.words('english')
	for w in word_arr:
		if w not in stop:
			if not w.isdigit():
				if w in d:
					d[w] += 1
				else:
					d[w] = 1
	return d

#remove words that overlap between paragraphs
#input: array of dictionaries
#output: only words not repeated between dictionaries
def rm_overlap(dict_arr):
	temp_dict_arr = []
	overall_dict = {}
	repeats_dict= {}
	for d in dict_arr:
		final_dict = {}
		for key in d:
			if key in overall_dict:
				if key in final_dict:
					del final_dict[key]
				#print "repeats"
				#print key
				repeats_dict[key] = 1
			else:
				if key not in repeats_dict:
					final_dict[key] = 1
					overall_dict[key] = 1
				else:
					if key in final_dict:
						del final_dict[key]
		temp_dict_arr.append(final_dict)
	final_arr = []
	for d in temp_dict_arr:
		temp_dict = {}
		for key in d:
			if key not in repeats_dict:
				temp_dict[key] = 1
			#temp_dict[key] = 1
			#for rep in repeats_dict:
				#if rep in key:
					#if key in temp_dict:
						#del temp_dict[key]
		final_arr.append(temp_dict)
	return final_arr

#the over-arching steps that bring together all the functions
def final_steps(para_arr_col):
	dict_arr = []
	for para_arr in para_arr_col:
		tok_arr = []
		for para in para_arr:
			tok_arr.extend(create_tokens(para))
		stopless_dict = rm_words(tok_arr)
		stopless_dict
		dict_arr.append(stopless_dict)
	"REMOVE OVERLAP"
	return rm_overlap(dict_arr)



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text, collec from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], collec=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute('insert into entries (title, text, collec) values (?, ?, ?)',
                 [request.form['title'], request.form['text'], request.form['collec']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/compare')
def compare():
	cur = g.db.execute('select title, text, collec from entries order by id desc')
	entries = [dict(title=row[0], text=row[1], collec=row[2]) for row in cur.fetchall()]
	#"Role in early bone the part embryogenesis."
	first_arr = []
	for ent in entries:
		first_arr.append([ent['text'],""])
	#first_arr = [[entries[0]['text'],""],[entries[1]['text'],""]]
	arr = final_steps(first_arr)
	print first_arr
	steps = []
	steps.append(arr)
	return render_template('show_entries.html', entries=entries, final=steps)



if __name__ == '__main__':
    app.run()