import re
import pickle as pkl

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

def inter_chunk_parser(filepath, pickle=False):	# filepath: ssh interchunk .dat file 
												# pickle = True if final data needs to be saved
	
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

			line = re.sub("'|>","",line)

			#--------------------------------------------------------------------
			if(line.startswith("<Sentence id=")):	# sentence block begins
				sent_flag = True	
				sent_id = int(re.sub("<Sentence id=","",line.rstrip('\n')))
				sent_obj = {"id":sent_id, "type":"sentence", "chunk_list":[]}
				continue

			#--------------------------------------------------------------------
			elif(line.startswith('</Sentence')):	# sentence block ends
				sent_flag = False	
				if(chunk_obj != {}):
						sent_obj["chunk_list"].append(chunk_obj)
						chunk_obj = {}
				data.append(sent_obj)
				continue

			#--------------------------------------------------------------------
			elif(sent_flag):	# inside sentence block
				line = re.split(' |\t', line.rstrip('\n'))

				#............................
				if(re.match('^[0-9]+$', line[0])):	# chunk block begins
					if(chunk_obj != {}):
						sent_obj["chunk_list"].append(chunk_obj)
						chunk_obj = {}
					# print(chunk_obj)
					chunk_obj = set_attr("chunk", line)
					chunk_obj["word_list"] = []
					continue

				#............................
				elif(re.match('^[0-9]+.[0-9]+$', line[0])):	# intra chunk word 
					word_obj = set_attr("word", line)
					word_obj["text"] = line[1]	#content of word is text form of word itself
					word_obj["drel"] = None
					if(word_obj != {}):
						chunk_obj["word_list"].append(word_obj)
						word_obj = {}
					continue

			#--------------------------------------------------------------------

		if(sent_id==-1):
			print(">> ERROR: No sentences detected")
		else:
			print(">> PARSER: "+str(sent_id+1)+" sentence(s) analyzed")

		if(pickle):
			file = open("parser_data.pkl", "wb")
			pkl.dump(data,file)
			print(">> PICKLE: parser data saved as pickle file")
			file.close()
	return data 

data = inter_chunk_parser("sample_inter_chunk.dat", pickle=False)

#Test
# for sent in data:
# 	print(sent["id"], end=" ")
# 	for chunk in sent["chunk_list"]:
# 		for word in chunk["word_list"]:
# 			print(word["text"], end=" ")
# 	print('\n')