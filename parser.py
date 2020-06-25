import re

def set_attr(obj_type, line):
	obj = {"type":None, "name":None, "tag":None, "drel":{"head":None, "reln":None}}
	for tok in line:
		obj["type"] = obj_type
		obj["tag"] = line[2]
		if(tok.startswith("name")):
			obj["name"] = re.sub("^name=","",tok)
		if(tok.startswith("drel")):
			drel = re.sub("^drel=","",tok)
			obj["drel"] = {"head":drel.split(":")[1], "reln":drel.split(":")[0]}
	return obj

def inter_chunk_parser(filepath):	# filepath: ssh interchunk .dat file
	
	data = []	# data: list of sent_dicts (sent_list)
	sent_flag = False	#indicates 'True' when file cursor inside a sentence block

#--------------------------------------------------------------------
	sent_id = -1	# sentence id [0-n]
	sent_obj = {}	# sentence dict {type, chunk_list}
	chunk_obj = {}	# chunk dict {type, name, tag, drel, word_list}
	word_obj = {}	# word dict {type, name, tag, drel, text}
#--------------------------------------------------------------------

	with open(filepath, 'r') as text:
		for line in text:

			line = re.sub("'>","",line)

			#--------------------------------------------------------------------
			if(line.startswith("<Sentence id=")):	# sentence block begins
				sent_flag = True	
				sent_id = len(data)
				sent_obj = {"type":"sentence", "chunk_list":[]}

			#--------------------------------------------------------------------
			elif(line.startswith('</Sentence')):	# sentence block ends
				sent_flag = False	
				data.append(sent_obj)

			#--------------------------------------------------------------------
			elif(sent_flag):	# inside sentence block
				line = re.split(' |\t', line.rstrip('\n'))

				#............................
				if(re.match('^[0-9]+$', line[0])):	# chunk block begins
					if(chunk_obj != {}):
						sent_obj["chunk_list"].append(chunk_obj)
					# print(chunk_obj)
					chunk_obj = set_attr("chunk", line)
					chunk_obj["word_list"] = []

				#............................
				elif(re.match('^[0-9]+.[0-9]+$', line[0])):	# intra chunk word 
					word_obj = set_attr("word", line)
					word_obj["text"] = line[1]	#content of word is text form of word itself
					word_obj["drel"] = None
					if(word_obj != {}):
						chunk_obj["word_list"].append(word_obj)
					# print(word_obj)

			#--------------------------------------------------------------------

		if(sent_id==-1):
			print(">> ERROR: No sentences detected")
		else:
			print(">> "+str(sent_id+1)+" sentences analyzed")
	return data 




data = inter_chunk_parser("sample_inter_chunk.dat")
