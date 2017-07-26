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
    task_msg = 'Welcome to the Flash Card Skill...Anytime in the game say change topic or change subtopic to change those respective elements... Are you ready to study?'

    session.attributes['state'] = 'start'  # conversation state we are in
    session.attributes['repetitions'] = 0  # how many times you have repeated the skill in one session
    session.attributes['correct'] = 0  # how many flashcards the user got correct
    session.attributes['topic'] = '' # the topic the user has chosen
    session.attributes['subtopic'] = '' # the subtopic the user has chosen

    session.attributes['state'] = 'start'
    return question(task_msg)


@ask.intent("YesIntent")
def choose_topic():
    if session.attributes['state'] == 'start':
        topic_msg = 'Which topic would you like to choose: Dates or Capitals'
        session.attributes['state'] = 'set_topic'
        return question(topic_msg)
    if session.attributes['state'] == 'check_topic':
        if session.attributes['topic'] == 'DATES':
            subtopic_msg = "Okay... Would you like American History or World History?"
        if session.attributes['topic'] == "CAPITALS":
            subtopic_msg = "Okay... Would you like United States or World Countries?"
        session.attributes['state'] = 'set_subtopic'
        return question(subtopic_msg)
    if session.attributes['state'] == 'check_subtopic':
        if session.attributes['subtopic'] == 'AMERICAN HISTORY':
            q = get_question('USDates.txt')
        if session.attributes['subtopic'] == 'WORLD HISTORY':
            q = get_question('WorldHistoryDates.txt')
        return question(q)


@ask.intent("SetTopicIntent")
def choose_subtopic(topic):
    if session.attributes['state'] == 'set_topic':
        if topic.upper() == 'DATES':
            session.attributes['topic'] = 'DATES'
            just_checking_msg = "You've picked dates. Is this correct?"
        elif topic.upper() == 'CAPITALS':
            session.attributes['topic'] = 'CAPITALS'
            just_checking_msg = "You've picked capitals. Is this correct?"
        session.attributes['state'] = 'check_topic'

    if session.attributes['state'] == 'set_subtopic':
        if topic.upper() == 'AMERICAN HISTORY':
            just_checking_msg = "You've picked American History. Is that the right topic?"
            session.attributes['subtopic'] = 'AMERICAN HISTORY'
        elif topic.upper() == 'WORLD HISTORY':
            just_checking_msg = "You've picked World History. Is that the right topic?"
            session.attributes['subtopic'] = 'WORLD HISTORY'
        if topic.upper() == 'UNITED STATES':
            just_checking_msg = "You've picked United States. Is that the right topic?"
            session.attributes['subtopic'] = 'UNITED STATES'
        elif topic.upper() == 'WORLD COUNTRIES':
            just_checking_msg = "You've picked World Countries. Is that the right topic?"
            session.attributes['subtopic'] = 'WORLD COUNTRIES'
        session.attributes['state'] = 'check_subtopic'

    return question(just_checking_msg)

@ask.intent("ChangeTopicIntent")
def change_topic_subtopic(change):
    print(change)
    if change.upper() == 'CHANGE TOPIC':
        session.attributes['state'] = 'start'
        msg = "Do you wish to change your topic? (Saying no will end the session)"
    if change.upper() == "CHANGE SUBTOPIC":
        session.attributes['state'] = 'check_topic'
        msg = "Do you wish to change your subtopic"
    return question(msg)

@ask.intent("NoIntent")
def all_done():
    if session.attributes['state'] == 'start':
        session.attributes['state'] = 'end'
        msg = "Oh well, you could have studied for once in your life ... Goodbye."
        return statement(msg)

    if session.attributes['state'] == 'check_topic':
        session.attributes['state'] = 'start'
        msg = "Do you wish to change your topic?"
        return question(msg)

    if session.attributes['state'] == 'check_subtopic':
        session.attributes['state'] = 'check_topic'
        msg = "Do you wish to change your subtopic"
        return question(msg)


if __name__ == '__main__':
    app.run(debug=True)
