# Group: Shiv, Marisa, and Sahana
# Alexa Skill: FlashCards
# Description: A program which has two categories and subcategories from
# which the user can choose to be tested on in the form of flashcards



import sys
import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_flashcards():
    session.attributes['welcome'] = 1
    prefix = 'Welcome to the Flash Card Skill... Are you ready to study?'

    session.attributes['state'] = 1  # conversation state we are in
    session.attributes['repetitions'] = 0  # how many times you have repeated the skill in one session
    session.attributes['correct'] = 0  # how many flashcards the user got correct

    task_msg = prefix
    session.attributes['state'] = 1
    return question(task_msg)

@ask.intent("NoIntent")
def all_done():
    # The user says no in the beginning
    if session.attributes['state'] == 1:  # origin state
        #(reminder for group)set the current state when coding later
        msg = "Oh well, you could have studied for once in your life ... Goodbye."

    return statement(msg)