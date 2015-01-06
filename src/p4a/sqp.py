import shlex
import re

_version=1
DEBUG=False

def parse(file):
	"""
	Takes file name as an argument and returns a root Klass instance containing all the data.
	"""
	lex = shlex.shlex(open(file))
	lex.wordchars += '.'
	tokens = list(lex);

	ks = [Klass(),]
	bs = []
	kw = ""
	vw = ""
	va = []
	arval = False
	i = 0
	while (i < len(tokens)):
		if DEBUG: print tokens[i]
		if (tokens[i] == "class" and tokens[i+1] != "="):
			if DEBUG: print "K"
			k = Klass(tokens[i+1])
			ks.append(k)
			bs.append(1)
			i+=3
		elif (tokens[i] == "{"):
			if DEBUG: print "KE"
			bs[-1]+=1
			i+=1
		elif (tokens[i] == "}"):
			
			bs[-1]-=1
			if bs[-1] == 0:
				if DEBUG: print "KL"
				k = ks.pop()
				ks[-1](k)
				bs.pop()
				i+=2;
			else:
				if DEBUG: print "KnL"
				i+=1
		elif not kw and not _kwp.search(tokens[i]):
			if DEBUG: print "kw"
			kw = tokens[i]
			if tokens[i+1] == "[":
				arval = True
				i+=4;
				va=[]
			else:
				arval=False
				vw=""
				i+=2
		elif tokens[i] == ";":
			if DEBUG: print "kve"
			if kw:
				if arval:
					ks[-1][kw] = va
				else:
					ks[-1][kw] = uq(value(vw))
				kw=""
			i+=1
		else:
			
			if arval:
				if tokens[i] != ",":
					if DEBUG: print "kva"
					va.append(uq(value(tokens[i])))
			else:
				if DEBUG: print "kvs"
				vw += tokens[i]
			i+=1
	return ks[0]

