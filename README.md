***************************Artificial Intelligence********************

**********************************Part-1******************************

The focus is to build a question-answering system.Few questions (queries) will be given. But
apart from these, there will be questions for each part that will have to be answered during
evaluation. So hard-coding should be avoided and your code should be as general as
possible.



=================================Dataset================================
For this phase, the commentary data of all the five ODI matches (for both innings) has to be
included.
The links to the 5 matches are:
1. http://www.espncricinfo.com/new-zealand-v-india-2014/engine/match/667641.html
2. http://www.espncricinfo.com/new-zealand-v-india-2014/engine/match/667643.html
3. http://www.espncricinfo.com/new-zealand-v-india-2014/engine/match/667645.html
4. http://www.espncricinfo.com/new-zealand-v-india-2014/engine/match/667647.html
5. http://www.espncricinfo.com/new-zealand-v-india-2014/engine/match/667649.html
________________________________________________________________________


===================Text processing========================================
This part deals with questions to be answered that will require string parsing and text
processing of the commentary data.
The commentary information consists of :
1. ball by ball details (so naturally over by over information is captured)
2. for each ball, the information is of the form:
PLAYER1 to PLAYER2, RUNS SCORED / “OUT”, DESCRIPTION (of the ball and the
way ball was played, etc).
3. comments by different users, during the course of play
So questions based on the following grammar need to be answered.
Rough grammar of questions for part 1:
<full question> : <info about match> <description> <question>
<info about match> : first | second | third | fourth | fifth
<description> : this will contain information about few / all of the following:
1. player hitting Ones / Twos / Fours / Sixes (optional number or
“maximum” ­ may be specified like player1 hit 3 sixes)
2. about the specific over(or there may not be any specific over given)3. player getting out
4. player bowling wide / no ball (optional number or “maximum” ­ may
be specified, see Q5)
<question> : which ball | which over | who dismissed (although this question can be
answered even using scorecard info) | who hit | which bowler
___________________________________________________________________________



=================================Questions==========================
1. In the first match, Kohli hit sixes in overs of which bowler(s)?
(here number of sixes and specific over is not specified, so you should retrieve all the instances)
2. In the first match, Williamson was out in which over?
(you will need to search for “OUT” word and find the appropriate over/ball information. In
this query the answer would be “NONE” as Williamson was not out, a clever solution would
be to first search the scorecard information and if required subsequently search the
commentary)
3. In third match, Taylor hit fours in which overs?
4. In fourth match, Dhoni hit six in over 30, in which ball?
5. In third match, Anderson bowled maximum wides in which over?
NOTE: These are sample questions, so you should follow the grammar rather than
hard-coding specific instances. Once you have the functions according to the grammar, you
have to call them for these examples, and for other questions which will be released at the
time of evaluation.


***************************PART-2 ************************************

Build the same engine without a question grammar.