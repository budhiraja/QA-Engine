import nltk,re
from nltk.tag.simplify import simplify_wsj_tag
from nltk.corpus import wordnet as wn
from en import verb as v


"""
Tag 	Meaning 	Examples

ADJ 	adjective 	new, good, high, special, big, local
ADV 	adverb 	really, already, still, early, now
CNJ 	conjunction 	and, or, but, if, while, although
DET 	determiner 	the, a, some, most, every, no
EX 	existential 	there, there's
FW 	foreign word 	dolce, ersatz, esprit, quo, maitre
MOD 	modal verb 	will, can, would, may, must, should
N 	noun 	year, home, costs, time, education
NP 	proper noun 	Alison, Africa, April, Washington
NUM 	number 	twenty-four, fourth, 1991, 14:24
PRO 	pronoun 	he, their, her, its, my, I, us
P 	preposition 	on, of, at, with, by, into, under
TO 	the word to 	to
UH 	interjection 	ah, bang, ha, whee, hmpf, oops
V 	verb 	is, has, get, do, make, see, run
VD 	past tense 	said, took, told, made, asked
VG 	present participle 	making, going, playing, working
VN 	past participle 	given, taken, begun, sung
WH 	wh determiner 	who, which, when, what, where, how

"""

indian_players = ["Dhawan", "Dhoni", "Aaron", "Ashwin", "Binny", "Jadeja", "Kohli", "Kumar", "Mishra", "Shami", "Rahane", "Raina", "Rayudu", "Sharma", "Sharma"]
nz_players = ["McCullum", "Anderson", "Benett", "Guptill", "Henry", "McClenaghan", "McCullum", "Mills", "Neesham", "Ronchi", "Ryder", "Southee", "Taylor", "Williamson", "Milne"]


cricket = [['dismissed' , 'out,'],['best','fine','classy','smooth'],['boundary','FOUR','SIX'],['weather','sunny','clear','hot','clouds','rain','shade','shady']]


def manage(question):
	if question.find("dismissed") != -1:
		question.replace("dismissed","OUT")
		#print question
	return question


class Ball:
	def __init__(self,rank,key,desc):
		self.rank = rank
		self.ball = key
		self.desc = desc
	def __str__(self):
		return str(self.rank) +"  " + self.desc

#result = {}
bolded_words = []


def parseFile(filename):
	lines_copy = []
	ballWise = {} # Dictionary for a ball by ball commentary
	widesAndNoballs = {} #Dictionary for Wides and No-balls
	ballNumber = re.compile("\d+.\d+") # Regular Expression to parse Balls
	rgcx1 = re.compile("\d+.\d+pm")
	rgcx2 = re.compile("\d+.\d+ pm")
	fileBuffer = "" # Buffer to hold the file
	#opening file to parse
	with open(filename) as fp:
	    for line in fp:
	    	fileBuffer = fileBuffer + line
	lines = fileBuffer.split('\n')
	lines_copy = lines[:]
	#print lines_copy
	for i in xrange(len(lines)):
		if i < len(lines) and not rgcx1.match(lines[i]) and not rgcx2.match(lines[i]) and  ballNumber.match(lines[i]):
			if lines[i] in ballWise.keys():
				if lines[i] in widesAndNoballs.keys():
					widesAndNoballs[str(float(lines[i])+0.1)] = ballWise[lines[i]]
				else:
					widesAndNoballs[lines[i]] = ballWise[lines[i]]
			j=i+3
			ballWise[lines[i]] = lines[j]
			while(j < len(lines) and not ballNumber.match(lines[j])):
				ballWise[lines[i]] = ballWise[lines[i]]+lines[j]
				j+=1
			lines.remove(lines[i+3])
			i+=3
			fileBuffer.replace(lines[i+3],"")
	lines = [item for item in lines if item not in ['','\t','\n'] and not ballNumber.match(item)]
	#print lines
	return ballWise,widesAndNoballs,lines, lines_copy


def find_in_lines(key_words,bold_words,IN,NZ):
	unigram_result = []
	for i in NZ:
		rank = 0
		for j in key_words:
			if i.find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,0,i)
			unigram_result.append(b)

	for i in IN:
		rank = 0
		for j in key_words:
			if i.find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,0,i)
			unigram_result.append(b)

	return unigram_result


def unigram(match,simplified,bold_words):
	unigram_result = []
	fileInd = "./dataset/odi"+str(match)+"_ininning.txt"
	fileNz = "./dataset/odi"+str(match)+"_nzinning.txt"
	key_words , question = create_tokens(simplified)
	ballWiseIn, widesAndNoballsIn = {} , {}
	ballWiseNz, widesAndNoballsNz = {} , {}
	ballWiseIn, widesAndNoballsIn, otherDataIn, all_linesIN = parseFile(fileInd)
	ballWiseNz, widesAndNoballsNz, otherDataNz, all_linesNZ = parseFile(fileNz)
	resultNz, resultIn = {} , {}
	key_words,question = create_tokens(simplified)
	key_words += find_related_words(bold_words)
	bold_words += find_related_words(bold_words)
	if ('weather' in key_words):
		unigram_result = find_in_lines(key_words,bold_words,all_linesNZ,all_linesIN)
		return unigram_result

	for i in ballWiseIn.keys():
		rank = 0
		for j in key_words:
			if ballWiseIn[i].find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,i,ballWiseIn[i])
			unigram_result.append(b)

	for i in ballWiseNz.keys():
		rank = 0
		for j in key_words:
			if ballWiseNz[i].find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,i,ballWiseNz[i])
			unigram_result.append(b)

	for i in widesAndNoballsIn.keys():
		rank = 0
		for j in key_words:
			if widesAndNoballsIn[i].find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,i,widesAndNoballsIn[i])
			unigram_result.append(b)

	for i in widesAndNoballsNz.keys():
		rank = 0
		for j in key_words:
			if widesAndNoballsNz[i].find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,i,widesAndNoballsNz[i])
			unigram_result.append(b)

	for i in otherDataNz:
		rank = 0
		for j in key_words:
			if i.find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,0,i)
			unigram_result.append(b)

	for i in otherDataIn:
		rank = 0
		for j in key_words:
			if i.find(j)!=-1:
				if j in bold_words:
					rank += 2
				else:
					rank += 1
		if rank > 0:
			b = Ball(rank,0,i)
			unigram_result.append(b)

	#for i in unigram_result:
	#	print i
	return unigram_result

def create_tokens(simplified):
	key_words = []
	question = ""
	for i in simplified:
		if i[1] not in ["TO", "DET", "CNJ", "MOD", "PRO", "." , "P", "NUM" ]:
			if i[0] not in ["was","were","match"]:
				key_words.append(i[0])
			if i[1] == "WH":
				question = i[0]
		if i[0] in ["out","dismissed"]:
			key_words.append("OUT,")
	#print "Key "
	return key_words,question


def remove_punctuation(s):
	s=s.translate(None, ",!.;")
	return s.lower()

def bigram_list(simplified):
	key_words = []
	for i in xrange(len(simplified)):
		if simplified[i][0] not in ["was","were","match","out"] and simplified[i][1] not in ["WH",'.']:
			if simplified[i-1][0] != "match" and simplified[i-1][1] != "NUM":
				key_words.append(simplified[i][0])
		if simplified[i][0] == "out":
			key_words.append("out")
	bigramFeatureVector = []
	for item in nltk.bigrams(key_words):
		bigramFeatureVector.append(' '.join(item))
	return bigramFeatureVector

def find_match(simplified):
	match = 0
	for i in xrange(len(simplified)):
		if simplified[i][0] == "match":
			return int(simplified[i+1][0])


def remove_from_list(lines,x):
	lines = [item for item in lines if item not in x ]
	return lines


def bigram(unigram_result,simplified):
	if ('<', 'NP') in simplified:
		simplified.remove(('<', 'NP'))
	if ('>', ':') in simplified:
		simplified.remove(('>', ':'))
	bigrams = bigram_list(simplified)
	print "Bigrams : "  + str(bigrams)
	bigram_result = []
	for i in unigram_result:
		for j in bigrams:
			tmp= remove_punctuation(i.desc)
			j= remove_punctuation(j)
			#print tmp
			if tmp.find(j)!=-1:
				i.rank += 3
				#bigram_result.append(i)
	return unigram_result


def find_related_words(words):
	result = []
	vehicle = []
	print "Words :" , str(words)
	for word in words:
		try:
			word = v.present(word)
		except:
			pass
		try:
			vehicle = wn.synset(word + '.n.01')
		except :
			try :
				vehicle = wn.synset(word + '.p.01')
			except:
				pass
		print vehicle
		if vehicle:
			tmp = list(set([w for s in vehicle.closure(lambda s:s.hyponyms()) for w in s.lemma_names]))
			result += [word] + tmp

			for w in cricket:
				if word in w:
					result += w

	return result




def find_bolded(question):
	result = []
	word_list = question.split()
	for i in word_list:
		if i[0]== '<':
			if i == "<dismissed>":
				result.append("OUT,")
			result.append(i[1:-1])
	
	return result

def calc_result(bigram_result,simplified):
	print "Best Anwsers"
	print "Over:Ball -> Rank"
	for i in bigram_result:
		if i.rank >1 and i.ball >0:
			print i.ball, "->" , i.rank
		if  i.rank >1 and i.ball ==0:
			print i.desc[:3] , "->" , i.rank
	question_tag = ""
	best_answers = []
	for i in simplified:
		if i[1] == "WH":
			question_tag = i[0]
	best_rank = 0
	if len(bigram_result) == 0:
		print "Sorry,can't answer"
	elif len(bigram_result) == 1:
		best_answers.append(bigram_result[0])
	else:
		for i in bigram_result:
			if i.rank >= best_rank:
				best_rank = i.rank
		for i in bigram_result:
			if i.rank == best_rank:
				best_answers.append(i)
	if question_tag == "When":
		overs = []
		for i in best_answers:
			overs.append(i.ball)
			print i.rank
		return remove_from_list(overs,[0])
	elif question_tag == "How":
		desc = []
		for i in best_answers:
			desc.append(i.desc)
		return desc
	elif question_tag in ["What","what"]:
		desc = []
		for i in best_answers:
			desc.append(str(i.rank) +"\t"+i.ball + "\t" +i.desc)
		return desc
	elif question_tag in ["Who","who","whose"]:
		verb = player_type(simplified)
		players = []
		if verb == "bowler" :
			for i in best_answers:
				tmp = i.desc.split()[0]
				if tmp in indian_players or tmp in nz_players:
					players.append(tmp)
					best_answers.remove(i)
		elif verb == "batsman":
			for i in best_answers:
				tmp = i.desc.split()[2]
				if tmp in indian_players or tmp in nz_players:
					players.append(tmp)
					best_answers.remove(i)
		if len(best_answers) > 0:
			for i in best_answers:
				flag = 0
				for j in indian_players:
					if i.desc.find(j) != -1:
						players.append(j)
						flag = 1
				for j in nz_players:
					if i.desc.find(j) != -1:
						players.append(j)
						flag = 1
				if flag ==1:
					best_answers.remove(i)

		return players
		

def player_type(simplified):
	for i in simplified:
		if i[0] in ["bowler","bowlers","bowled"]:
			return "bowler"
		elif i[0] in ["batsman","batsmen"]:
			return "batsman"

def nounPhrase(simplified):
	result = []
	for i in simplified:
		if i[1] == "NP":
			result.append(i[0])
		print i
	return result

def main():
	question = raw_input()
	#question = "How was Ryder <OUT,> in match 1?"
	bold_words = find_bolded(question)
	question = question.replace('<',"")
	question = question.replace('>',"")
	print question
	
	question = manage(question)
	tokenized = nltk.word_tokenize(question)
	tagged = nltk.pos_tag(tokenized)
	simplified = [(word, simplify_wsj_tag(tag)) for word, tag in tagged]
	print simplified
	bold_words += nounPhrase(simplified)
	print bold_words
	match = find_match(simplified)	
	result = unigram(match,simplified,bold_words)
	#print result
	result = bigram(result,simplified)
	#for i in result:
	#	print i
	best_answers = result
	player = ""
	for i in simplified:
		if i[0].istitle():
			if i[0] in indian_players or i[0] in nz_players:
				player = i[0]
	if player != "":
		for i in best_answers:
			if i.desc.find(player) != -1:
				i.rank += 2
	print calc_result(best_answers,simplified)

main()
