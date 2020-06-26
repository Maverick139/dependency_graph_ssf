import ssfparser as sfp

def dotconstr(sent_id, vertices, edges, save=False):
	if(len(vertices)-len(edges)!=1):
		print(">> DOTCONSTR: Invalid number of vertices and edges to contruct tree ( Sent_ID:"+str(sent_id)+" ; V:"+str(len(vertices))+" ; E:"+str(len(edges))+")")
	infile = open("temp.dot",'w')
	content = ['digraph {\n']+vertices+edges+['}\n']
	infile.writelines(content)
	infile.close()

def extract_chunk_text(chunk):
#returns words contained in chunk, in single str format
	text = ""
	for word in chunk["word_list"]:
		text += word["text"]+" "
	return text.rstrip(" ")

def interconvdotformat(data, save=False):	#generator func : yields dot file
#converts eah sent in data(dict) to individual inter_chunk_graph dot files (compatible with Graphviz)

	for sent in data:
		vertices = []	#vertices of dep_graph	{ <chunk> }
		edges = []	#edges of dep_graph	{ <head> -> <chunk> [reln] }
		sent_id = sent["id"]
		chunk_list = sent["chunk_list"]
		for chunk in chunk_list:
			chunk_text = extract_chunk_text(chunk)
			chunk_vertex = '\t'+chunk['name']+' [label="'+chunk_text+' ('+chunk['tag']+')"]\n'
			vertices.append(chunk_vertex)	#store each chunk as a graph vertex
			if(chunk['drel']['head'] != None):
				chunk_edge = '\t'+chunk['drel']['head']+' -> '+chunk['name']+' [label="'+chunk['drel']['reln']+'"]\n'
				edges.append(chunk_edge)	#store each chunk-head reln as a graph edge
		dotfilepath = dotconstr(sent_id, vertices, edges, save)
		yield sent_id, dotfilepath

# data = sfp.inter_chunk_parser("sample_inter_chunk.dat")
# for sent_id, path in interconvdotformat(data):
# 	print("s_id: ",sent_id)
# 	input("press Enter to move to next sentence")


# def view_sent(sent_id, data):
# 	for sent in data:
# 		if(sent["id"]==sent_id):
# 			print("No.of chunks: "+str(len(sent["chunk_list"])))
# 			for chunk in sent["chunk_list"]:
# 				print(chunk["name"],chunk["drel"]["head"],chunk["drel"]["reln"],"\n\n")

# view_sent(16,data)