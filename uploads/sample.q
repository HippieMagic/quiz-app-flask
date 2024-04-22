* SAMPLE QUIZ QUESTIONS
* Jim Mooney
* CS 533

* This is a question file for the quiz program.
* Any line that begins with an asterisk should be ignored.
* Totally blank lines should also be ignored.

* The file consists of a sequence of questions.
* Each question has the following form:
*
*	1. A line beginning with "@Q".
*	2. Up to ten lines giving the text of the question.
*	3. A line beginning with "@A"
*	4. A line consisting of the integer value for the correct answer
*	5. Up to ten lines giving answer choices, one line each.
*	6. A line beginning with "@E".
*
* The question file has the form of a sequence of variable-length
* text lines, Each containing 75 characters or fewer.  The character
* code and the detailed form of the file (line terminators, etc.) are
* those conventional for the system on which it is installed.
*
* The following example file contains two questions.  The first has
* four possible answers; the correct answer is the second.  The second
* has six possible answers; the correct answer is the fourth.

@QUESTIONS
How many class days are there in this entire term?
@ANSWERS
2
forty-one
twenty-nine
seems like hundreds
who's counting?
@END

@QUESTION

This is a long question which rambles on with no apparent end in sight.
It has two purposes.  The first is to catch those of you who have not
provided enough buffer space for a very long question.  The second is to
ask you to figure out how many letters there are (not counting spaces or
punctuation marks) in this entire paragraph.

@ANSWERS
4
509
266
1066
263
None of the above
All of the above
@END
* Remember: blank lines and comments are ignored throughout!

* END OF FILE





