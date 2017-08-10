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
    task_msg = 'Welcome to the Flash Card Skill created at CMU in the Summer Academy for Math and Science...Say change topic, change subtopic, or cancel anytime... Are you ready to study?'

    resetVars()

    session.attributes['state'] = 'start'
    return question(task_msg)

def resetVars():
    session.attributes['state'] = 'start'  # conversation state we are in
    session.attributes['repetitions'] = 0  # how many times you have repeated the skill in one session
    session.attributes['correct'] = 0  # how many flashcards the user got correct
    session.attributes['question'] = ''
    session.attributes['answer'] = ''
    session.attributes['topic'] = ''  # the topic the user has chosen
    session.attributes['subtopic'] = ''  # the subtopic the user has chosen
    session.attributes['fileName'] = ''
    session.attributes['fileList'] = []
    session.attributes['tryAgain'] = 0

@ask.intent("YesIntent")
def choose_topic():
    if session.attributes['state'] == 'start':
        topic_msg = 'Which topic would you like to choose: Dates or Capitals'
        session.attributes['state'] = 'set_topic'
        return question(topic_msg)
    if session.attributes['state'] == 'set_topic':
        if session.attributes['topic'] == 'DATES':
            subtopic_msg = "Would you like American History or World History?"
        elif session.attributes['topic'] == 'CAPITALS':
            subtopic_msg = "Would you like United States or World Countries?"
        session.attributes['state'] = 'set_subtopic'
        return question(subtopic_msg)
    if session.attributes['state'] == 'tryAgain':
        session.attributes['tryAgain'] += 1
        repeat_question = session.attributes['question']
        return question(repeat_question)


@ask.intent("SetTopicIntent")
def choose_subtopic(topic):
    if session.attributes['state'] == 'set_topic':
        if topic.upper() == 'DATES':
            session.attributes['topic'] = 'DATES'
            subtopic_msg = "Great Dates...Would you like American History or World History?"
        elif topic.upper() == 'CAPITALS':
            session.attributes['topic'] = 'CAPITALS'
            subtopic_msg = "Great Capitals...Would you like United States or World Countries?"
        session.attributes['state'] = 'set_subtopic'
        return question(subtopic_msg)
    if session.attributes['state'] == 'set_subtopic':
        if topic.upper() == 'AMERICAN HISTORY':
            just_checking_msg = "You've picked American History."
            session.attributes['subtopic'] = 'AMERICAN HISTORY'
            session.attributes['fileName'] = 'USDates.txt'
            session.attributes['fileList'] = get_question(session.attributes['fileName'])
        elif topic.upper() == 'WORLD HISTORY':
            just_checking_msg = "You've picked World History."
            session.attributes['subtopic'] = 'WORLD HISTORY'
            session.attributes['fileName'] = 'WorldHistoryDates.txt'
            session.attributes['fileList'] = get_question(session.attributes['fileName'])
        if topic.upper() == 'UNITED STATES':
            just_checking_msg = "You've picked United States."
            session.attributes['subtopic'] = 'UNITED STATES'
            session.attributes['fileName'] = 'USCapitals.txt'
            session.attributes['fileList'] = get_question(session.attributes['fileName'])
        elif topic.upper() == 'WORLD COUNTRIES':
            just_checking_msg = "You've picked World Countries."
            session.attributes['subtopic'] = 'WORLD COUNTRIES'
            session.attributes['fileName'] = 'WorldCapitals.txt'
            session.attributes['fileList'] = get_question(session.attributes['fileName'])
        session.attributes['state'] = 'ask_question'
        return question(just_checking_msg + " " + ask_question())


def ask_question():
    index = randint(0,len(session.attributes['fileList'])-1)
    q, a = session.attributes['fileList'].pop(index)
    session.attributes['question'] = q
    session.attributes['answer'] = a
    session.attributes['state'] = 'question'
    return q


@ask.intent("ChangeTopicIntent")
def change_topic_subtopic(change):
    if change.upper() == 'CHANGE TOPIC':
        session.attributes['state'] = 'set_topic'
        resetVars()
        msg = "sure...Which topic would you like: Dates or Capitals"
    if change.upper() == "CHANGE SUBTOPIC":
        session.attributes['state'] = 'set_subtopic'
        topic = session.attribute['topic']
        resetVars()
        session.attributes['topic'] = topic
        if session.attributes['topic'].upper() == "DATES":
            msg = "sure...Would you like American History or World History?"
        elif session.attributes['topic'].upper() == "CAPITALS":
            msg = "sure...Would you like United States or World Countries?"
    return question(msg)


@ask.intent("CheckAnswerIntent")
def check_answer(answer):
    print(answer)
    if session.attributes['state'] == 'question' or session.attributes['state'] == 'tryAgain':
        if session.attributes['answer'].upper() == answer.upper():
            session.attributes['correct'] += 1
            session.attributes['repetitions'] += 1
            session.attributes['tryAgain'] = 0
            if session.attributes['repetitions'] < 6:
                return question("Good Job, that's correct." + " On to the next question..." + ask_question())
            else:
                if session.attributes['correct'] <= 2:
                    return statement("The study session is done. Your correct number of answers is " +str(session.attributes['correct']) + 'out of five...Do you want to play again.')
                elif session.attributes['correct'] > 2:
                    return statement("...Great Job...The study session is done. Your correct number of answers is " + str(session.attributes['correct']) + 'out of five...Do you want to play again.')

        # string interpolation %
        else:
            try_again_msg = 'Do you want to try again?'
            if not session.attributes['state'] == 'tryAgain':
                session.attributes['repetitions'] += 1
            if session.attributes['repetitions'] < 6:
                if session.attributes['tryAgain'] < 2:
                    session.attributes['state'] = 'tryAgain'
                    return question("I'm sorry, that's not correct..." + " " + try_again_msg)
                else:
                    session.attributes['tryAgain'] = 0
                    return question("I'm sorry, that's not correct." + " The correct answer is " + session.attributes['answer'] + "... On to the next question... " + ask_question())
            else:
                if session.attributes['correct'] <= 2:
                    return statement("The study session is done. Your correct number of answers is " +str(session.attributes['correct']) + 'out of five...Do you want to play again.')
                elif session.attributes['correct'] > 2:
                    return statement("...Great Job...The study session is done. Your correct number of answers is " + str(session.attributes['correct']) + 'out of five...Do you want to play again.')
                # string interpolation %
    else:
        session.attributes['state'] = 'start'
        resetVars()
        return question("Sorry I didn't understand that. Do you wish to restart the game")

@ask.intent("NoIntent")
def all_done():
    if session.attributes['state'] == 'start':
        session.attributes['state'] = 'end'
        msg = "Please come back to study soon... Goodbye!."
        return statement(msg)

    """if session.attributes['state'] == 'check_topic':
        session.attributes['state'] = 'start'
        msg = "Do you wish to change your topic?"
        return question(msg)

    if session.attributes['state'] == 'check_subtopic':
        session.attributes['state'] = 'check_topic'
        msg = "Do you wish to change your subtopic"
        return question(msg)"""

    """if session.attributes['state'] == 'question':
        return statement(session.attributes['answer'])"""
    
    if session.attributes['state'] == 'tryAgain':
        return question("Alright, next question..." + ask_question())


@ask.intent("AMAZON.CancelIntent")
def end_game():
    end_msg = "Thanks for playing...Goodbye"
    return statement(end_msg)


@ask.intent("AMAZON.StartOverIntent")
def repeat_game():
    session.attributes['state'] = 'start'
    resetVars()
    return question("Do you wish to start over (Saying no will end the study session)")


def get_question(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    qa = [tuple(qa.strip().split('+')) for qa in lines]
    """index = randint(0,24)
    q = qa[index][0]
    a = qa[index][1]
    session.attributes['answer'] = a
    session.attributes['state'] = 'question'"""
    return qa

if __name__ == '__main__':
    app.run(debug=True)
