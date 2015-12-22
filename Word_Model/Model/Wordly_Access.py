# Wordly_Access.py
# For initiating/calling the model

from Wordly import Wordly
import os

# Initialize on run
rnn = Wordly()

print rnn.look_up("being one more than one")

# Receive queries


# Return results
os.write(3, '{"dt" : "This is a test"}' + "\n", "utf8")


# http://stackoverflow.com/questions/23804434/python-process-forked-by-nodejs-alternative-to-process-send-for-python?rq=1

# var child = child_process.spawn('python', ['hello.py'], {
#   stdio:[null, null, null, 'ipc']
# });

# child.on('message', function(message) {
#   console.log('Received message...');
#   console.log(message);
# });