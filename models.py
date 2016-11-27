try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import numpy as np
############
n = 300
############

from gensim.models.word2vec import Word2Vec
import os

DBNAME = os.environ['flight2vec_DBNAME']
DBUSER = os.environ['flight2vec_DBUSER']
DBPASS = os.environ['flight2vec_DBPASS']
DBHOST = os.environ['flight2vec_DBHOST']


db = pymysql.connect(host=DBHOST,user=DBUSER,passwd=DBPASS,db=DBNAME)
c=db.cursor()
query = """SELECT FDE_CODE as codice,`FDE Text` as descr FROM newdata group by FDE_CODE
UNION
SELECT MESSAGE_CODE as codice,`Message Text` as descr FROM newdata group by MESSAGE_CODE"""
c.execute(query)
result = c.fetchall()
dictionary={item[0]:item[1].decode('latin1','ignore') for item in result}
db.close()
dictionary['exception']='Not enough data to find similar entities.'


def filter_codes(text):
	db = pymysql.connect(host=DBHOST,user=DBUSER,passwd=DBPASS,db=DBNAME)
	c=db.cursor()
	query = """SELECT FDE_CODE as codice,`FDE Text` as descrizione FROM newdata where FDE_CODE like '"""  + text + """%' group by FDE_CODE LIMIT 500
	UNION
	SELECT MESSAGE_CODE as codice,`Message Text` as descrizione FROM newdata where MESSAGE_CODE like '""" + text + """%' group by MESSAGE_CODE LIMIT 500 """
	c.execute(query)
	result = c.fetchall()
	lista=[item[0] + ": " + item[1].decode('latin1','ignore') for item in result]
	db.close()
	return lista

def get_top(code,n=300):
	model = Word2Vec.load('flight2vec/1leg_%dfeatures_nonuisc.w2v' % n)
	results = dict()
	results['fdes'] = [('exception',0)]
	results['msgs'] = [('exception',0)]
	try:
		l = model.most_similar(positive=[code.replace(' ','_')],topn=200)
	except:
		return (results,dictionary)

	results['fdes'] = [(x[0].replace('_',' '),x[1]) for x in l if x[0][3]=='_'][:10]
	results['msgs'] = [x for x in l if x[0][3]!='_'][:10]
	return (results,dictionary)

