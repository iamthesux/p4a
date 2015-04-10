import shlex
import re

from . import Klass, pvalue, _kwp, uq, value

DEBUG = False

class Writer(object):
	def __init__(self, f):
		if type(f) is str:
			self.stream = open(f, 'wb')
		else:
			self.stream = f
	
	def write(self, rap, d=0):	
		if rap.name:
			if rap.delete:
				self.stream.write(("\t"*(d-1)) + "delete " + rap.name)
			else:
				self.stream.write(("\t"*(d-1)) + "class " + rap.name)
			if rap.inherits:
				self.stream.write(' : ' + rap.inherits)
			if not (rap.extern or rap.delete):
				self.stream.write("\n" + ("\t"*(d-1)) + "{\n")
		for k,v in rap._data.items():
			if isinstance(k, Klass):
				self.write(k, d+1)
			else:
				self.stream.write(("\t"*d)+ k)
				if isinstance(v, list):
					self.stream.write("[]=")
					if len(v) == 0:
						self.stream.write('{}')
					elif (isinstance(v[0], str) and len(v) > 2) or len(v) > 3:
						self.stream.write("\n" + ("\t"*d) + "{\n")
						tmp = ",\n" + ("\t"*(d+1))
						self.stream.write(("\t"*(d+1)) + tmp.join(map(pvalue, v)) + "\n" + ("\t"*d) + "}")
					else:
						self.stream.write("{" + ", ".join(map(pvalue,v)) + "}")
				else:
					self.stream.write("=" + pvalue(v))
				self.stream.write(";\n")
		if rap.name:
			if not (rap.extern or rap.delete):
				self.stream.write(("\t"*(d-1)) + "}")
			self.stream.write(";\n")

class Reader(object):
	def __init__(self, f):
		if type(f) is str:
			self.stream = open(f, 'r')
		else:
			self.stream = f
	def read(self):
		lex = shlex.shlex(self.stream)
		lex.wordchars += '-.'
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
				if DEBUG: print "K: %s" % tokens[i+1]
				k = Klass(tokens[i+1])
				
				if DEBUG: print "TK: %s" % tokens[i+2]
				if tokens[i+2] == ';':
					k.extern = True
					ks[-1](k)
				else:
					if tokens[i+2] == ':':
						k.inherits =  tokens[i+3]
						i+=2
					bs.append(1)
					ks.append(k)
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


	