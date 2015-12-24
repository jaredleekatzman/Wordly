# Wordly_Init.py
# For initiating/calling the model

from Wordly import Wordly
import os
import sys
import json
from socketIO_client import SocketIO

with SocketIO('54.152.167.250', 8000) as socketIO:
    # socketIO.emit('aaa')
    # socketIO.wait(seconds=1)

	# Phase 0
	# os.write(3, '{"dt" : "This is a test"}')

	socketIO.emit('test', '{"dt" : "This is a test"}')

	# Initialize on run
	rnn = Wordly()
	rnn.initialize_model(json = 'Word_Model/Model/model.json', 
	        weights = 'Word_Model/Model/weights.hdf5',
	        embed_path = 'Word_Model/Model/embeddings.hdf5', verbose = False)

	output = rnn.look_up(sys.argv[1])

	# output = [("Silurian", 0.80866586826121223), ("Paleozoic", 0.84940722613702724), ("Palaeolithic", 0.95937944007114762), ("Cenozoic", 0.96295106505316119), ("Mesolithic", 1.0181287210346959)]

	result = {}
	best = output.pop()
	result["best"] = best[0]
	result["score"] = best[1]
	result["others"] = output

	# print sys.argv[1]
	# print res[1]

	socketIO.emit('result', json.dumps(result))

	# while True:
	# 	# Phase 1
	# 	# result = json.loads(rnn.look_up(sys.argv[1]))
	# 	# json.dump(result,3)

	# 	res = rnn.look_up(sys.argv[1])
	# 	# json.dump(res,2)
	# 	print res
	# 	socketIO.emit(res)

	# 	# Phase 2
	# 	def query(str):
	# 		result = rnn.look_up(str)

	# 		primary = result[0][0]
	# 		primary_score =  result[0][1]

	# 		print result
	# 		print primary
	# 		print primary_score


