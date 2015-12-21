This is the readme.txt file for Project Gutenberg #29765.


Transcriber's note:

This file is about 27.4 Meg (it is the electronic version of that
massive tome that college libraries like to enshrine on their own
individual lecterns), so you will need a good text editor to
handle it.  Notepad simply will not do.  I strongly recommend that
you get the freeware NoteTab Light, which you can download at
http://www.notetab.com/downloads.php

I recommend this not least because NoteTab includes its own
scripting language, and I have provided a couple of scripts that
automate the lookup process for you (see Automatic Lookup below).

When you have installed NoteTab, you will find an option on its
Help menu saying Replace MS Notepad, and you should click that
option.  But be warned, with its customary devotion to user
convenience, Microsoft has included code in later versions of
Windows that prevents this. If you click it and Replace MS Notepad
does not get dimmed out then you are out of luck.  If you still
want to make a shortcut to Dictionary.txt and put it on your
desktop, you will need to change the file association for .txt
files.  To do this in XP open My Documents, click the Tools menuu
and click Folder Options.  In Folder Options click the File Types
tab and scroll down to the TXT Extension. Select it and below it
will probably say Opens with Notepad.  Click Change and in the
Open With window select NoteTab Light and be sure that "Always use
the selected program to open this type of file" is checked.  Then
click Okay.


This dictionary is Webster's 1913 edition, so it does not include
any modern words.  However, it has two major virtues for which you
may prefer it.

1) If you read a lot of Project Gutenberg editions, it has the
spellings you are likely to encounter in the books you read.

2) As a passive file it can be browsed much like a paper
dictionary, e. g. you can use it to find words that you are not
sure how to spell (see Manual Lookup below for details).

If you want a freeware modern dictionary, Princeton provides
Wordnet which you can download at
http://wordnet.princeton.edu/wordnet/download
You may want to download this even if you intend to use Webster's,
because the scripts I mentioned above for automatic lookup will
automatically turn to Wordnet if they don't find your word in
Webster's.

To facilitate those scripts, I recommend you choose the default
options when you install Wordnet, and that you put the Webster1913
folder in My Documents.  If you put them anywhere else, or if you
change the name of the file to other than 29765-8.txt, then
you will need to make changes to the scripts to get them to work.
This is detailed below under Error Message.


Manual Lookup

Double click the 29765-8.txt shortcut that you put on your
desk top. When it has loaded, about 30 seconds, press Ctrl+F to
invoke the Find function.  Enter your word in ALL CAPITALS, check
Whole Words and Case Sensitive, and press Enter.  If the first
definition it finds is not the one you seek, press Enter again.

If you find this process rather tiresome when looking up really
short words (1 or 2 letters), surround the word with ^P (e.g.
^POF^P) and search for that instead (NoteTab interprets ^P as a
line-break).

If you want to look up a word but are not sure of its spelling,
you can look up a fragment of the word. Enter as much of the word
as you are sure of in capitals, check Case Sensitive and UNCHECK
Whole Word.  Press Enter repeatedly until you reach the part of
the dictionary that you want to browse.


Automatic Lookup

From this folder copy 29765.clb into NoteTab Light's
Libraries folder.  Start NoteTab.  Along the bottom of the screen
you will see a row of buttons in alphabetical order.  If the
Webster1913 button is not visible click the Right Arrow at the
extreme right of this row until Webster1913 comes into view.
Click the Webster1913 button so that it is depressed.  Now you are
ready.

If you are reading a text file in NoteTab, position the cursor at
the left end of, or in the word of interest and press Esc n Enter.
If you want to look up a phrase, select it so that at least part
of the first and last words are included in the selection, and
press Esc n Enter.

If you are reading in a different program, select the word or
phrase in its entirety and copy to the clipboard.  Switch to
NoteTab and press Esc p Enter.

N. B. Webster1913 only lists the root word as a target, so you
cannot use it to find plurals, present or past participles, etc
(-s, -ing, -ed forms).  To look these up automatically, select just
that part of the word that forms the root, copy it to the
clipboard and Esc p Enter.  For forms that do not include the
whole root, e. g. continuing, you must use Manual Lookup for the
root.

If your word or phrase cannot be found in Webster1913 the script
will then access WordNet and search for it there.


Error Message

If the script cannot locate either of the dictionaries you will
get an error message and will have to change the scripts to  show
their true paths.
In NoteTab open ...\NoteTab Light\Libraries\29765.clb.

If 29765-8.txt cannot be found locate the ^!Open statement
near the start of both scripts.  Change the part inside the quotes
to the true full file path.
To get this right-click the shortcut to 29765-8.txt and click
Properties, then copy the highlighted Target.

If Wordnet cannot be found locate the ^!ChDir statement towards
the end of both scripts and change the part in quotes to the
correct directory for wnb.exe.  Again right-click the shortcut,
click Properties and copy the highlighted path.

In both cases be sure the path is bounded by quotes, and by only
one set of quotes.

If you do not intend to install WordNet and want to stop the
scripts from giving you an error message every time they try to
start it, then locate the ^!Prompt about a quarter of the way up
from the end of both scripts.  Insert a semi-colon (;) at the
start of that line and save the file.  The scripts will now just
terminate silently if your word is not found.


Caveat

This edition of Webster's is an ongoing project and currently is
full of errors.  There are many typos and some pages from the
original text are completely missing, so if you do not find a word
that you are sure was current in 1913, this is probably why.  If
you find an error, or a target-word (all capitals) that is
misspelled, please let me know about it, graham.lawrence@yahoo.com
If you would like to assist Project Gutenberg with this or another
project click the link "start here" at the top right of
http://www.gutenberg.org/wiki/Main_Page



HISTORY

*** Phase 2 completed 8/17/2009 ***

Added more than 4000 new words.

Corrected misspellings of more than 1000 target words, and their
definitions.

Restored 29765-8.txt to its natural sequence as in the paper
edition.  This is not Ascii sequencing, Webster's originaly
sequenced the file in an order in which only letters of the
alphabet had significance.  This allows forms like -ABLE to occur
in the same group as ABLE, rather than off on their own.

Tweaked the scripts in 29765.clb to enable unerring lookup
of very short words (1 or 2 letters).
If you use automatic lookup you should replace your existing
29765.clb in NoteTab's Libraries folder with this new one.

*** Phase 1 completed 7/30/2009 ***

From the original html in pgwht04.txt:

Converted all target words to upper-case

Replaced \'xx and & ... : special character code forms in target
words to their upper-case plain text equivalent.

Replaced \'xx and & ... : special character code forms in the body
of the text to their appropriate case Ascii equivalent.

Removed about 4 Meg of repeated garbage html identified by the
form <Xpage=< ... >>

Identified and corrected more than 1300 ambiguous target words.

Removed html codes.

Reformatted resultant text to improve readibility.


TO DO

Standardize format of entries in 29765-8.txt to a minimum of

Target word line
One or more lines of Pronunciation and Etymology
Blank line
One or more lines of Definition
Blank line

To which may be added multiple Definitions, Synonyms, Antonyms and
Notes, each group followed by a blank line.


Format tables, currently these have no formatting at all

Remove corrupt pronunciation codes


