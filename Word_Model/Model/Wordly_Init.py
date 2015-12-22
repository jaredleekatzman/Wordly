# Wordly_Init.py
# For initiating/calling the model

from Wordly import Wordly
import os
# import sys

# Initialize on run
rnn = Wordly()
rnn.initialize_model()

# return 0
# Wordly.look_up(sys.argv[1])
# Receive queries

# Return results
# os.write(3, '{"dt" : "This is a test"}' + "\n", "utf8")

# print "b4"

# os.write(3, "This is a test")

# print "a4tr"
# http://stackoverflow.com/questions/23804434/python-process-forked-by-nodejs-alternative-to-process-send-for-python?rq=1

# var child = child_process.spawn('python', ['hello.py'], {
#   stdio:[null, null, null, 'ipc']
# });

# child.on('message', function(message) {
#   console.log('Received message...');
#   console.log(message);
# });