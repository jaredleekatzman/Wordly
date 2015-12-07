# Wordly
ADS Project

## Task List:
- (Tim) Download dictionaries and write a script to get them all into the same format
- (Jared) Run word2vec on a larger corpus (NYTimes / Wikipedia / > 100 MB from tutorial)
- Implement simple RNN using word2vec embedding and dictionary training/test set

## AWS Access:
ssh -i <key> ec2-user@54.152.167.250

## bashrc
sudo vim /etc/bashrc
change this line to:
[ "$PS1" = "\\s-\\v\\\$ " ] && PS1="\[\e[0;36m\]$NICKNAME:\[\e[m\] \[\e[1;31m\]\W\[\e[0m\] > "