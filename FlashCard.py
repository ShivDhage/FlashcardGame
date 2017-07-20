# Group: Shiv, Marisa, and Sahana
# Alexa Skill: FlashCards
# Description: A program which has two categories and subcategories from
# which the user can choose to be tested on in the form of flashcards

#hi

import sys
import logging
#You might need this to get a random card for the user! But that's later on -PH
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_flashcards():

    session.attributes['welcome'] = 1
    task_msg = 'Welcome to the Flash Card Skill... Are you ready to study?'

    session.attributes['state'] = 'start'  # conversation state we are in
    session.attributes['repetitions'] = 0  # how many times you have repeated the skill in one session
    session.attributes['correct'] = 0  # how many flashcards the user got correct

    session.attributes['state'] = 'start' # sets state to 'start'
    return question(task_msg) # alexa asks if you are ready


@ask.intent("YesIntent")
def choose_topic():
    if  session.attributes['state'] == 'start': # checks if state is 'start'
        topic_msg = 'Which topic would you like to choose: Dates or Capitals'
        session.attributes['state'] = 'set_topic'
        return question(topic_msg) # alexa asks you which topic you want to choose

@ask.intent("SetTopicIntent")
def choose_subtopic(topic):
    
    if(session.attributes['state'] == 'set_topic'):
        if topic.upper() == 'DATES': #(error message) alexa not recognizing dates try .equals or something else
            subtopic_msg = 'Which subtopic would you like to study: American History or World History '
        elif(topic.upper() == ('CAPITALS')):  #(error message) alexa not recognizing dates try .equals or something else
            subtopic_msg = 'Which subtopic would you like to study: United States or World Countries'
        session.attributes['state'] = 'set_subtopic'
    if(session.attributes['state'] == 'set_subtopic'):
        if(topic.upper() == 'AMERICAN HISTORY'):
            subtopic_msg = "You've picked American History. Is that the right topic?"
        elif topic.upper() == 'WORLD HISTORY':
            subtopic_msg = "You've picked World History. Is that the right topic?"
    return question(subtopic_msg) # alexa asks you sub topic or if you wish to continue based on incoming state
    """
    print(topic)
    return statement(topic)"""

@ask.intent("NoIntent")
def all_done():
    if session.attributes['state'] == 'start': # checks if state is 'start'
        #(reminder for group)set the current state when coding later
        msg = "Oh well, you could have studied for once in your life ... Goodbye."
        return statement(msg)


#This is something you have to add! I'll talk about it later today.
#End comment

if __name__ == '__main__':
    app.run(debug=True)
