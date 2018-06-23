import random

def getMathQuestion(minNum, maxNum, types):
    
    '''Generates a math question for the function'''
    
    firstNum = random.randint(minNum,maxNum)
    secondNum = random.randint(minNum,maxNum)
    #Types should be a list containing one or more of 'plus', 'minus',
    #'times'
    mathType = random.choice(types)
    
    if mathType == 'plus':
        correctAnswer = firstNum + secondNum
    elif mathType == 'minus':
        correctAnswer = firstNum - secondNum
    elif mathType == 'times':
        correctAnswer = firstNum * secondNum

    #Create the question string and return the necessary info
    outStr = '{0} {1} {2}'.format(str(firstNum), mathType, str(secondNum))
    return (correctAnswer, outStr, firstNum, mathType, secondNum)

def mathPractice_launch(event, context):
    
    '''Launches the Math Practice Alexa skill.'''
    
    outStr = "<speak>I'll tell you a math question. Don't say Alexa, just say your answer. " + \
            "I'll tell you if you're right or wrong, and then give you another question. " + \
            "Say the word <break time='200ms'/>ready<break time='200ms'/> " + \
            "to start the session, the word " + \
            "<break time='200ms'/>restart<break time='200ms'/> to " + \
            "restart the session, and the word " + \
            "<break time='200ms'/>done<break time='200ms'/> or " + \
            "<break time='200ms'/>stop<break time='200ms'/> to end the session.</speak>"
            
    outCardStr = "I'll tell you a math question. Don't say Alexa, just say your answer. " + \
            "I'll tell you if you're right or wrong, and then give you another question. " + \
            "Say the word ready to start the session, the word " + \
            "restart to restart the session, and the word " + \
            "done or stop to end the session."

    #Python dictionary with the response information.  Keep the session alive.
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "numRight": 0,
            "numTotal": 0
        },
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": outStr
            },
            "card": {
                "type": "Simple",
                "title": "Math Practice",
                "content": outCardStr
            },
            "reprompt": {
                "outputSpeech": {
                "type": "PlainText",
                "text": "Are you ready to begin?"
                },
            },
            "shouldEndSession": 'false'
        }
    }
    return response
    
def mathPractice_startPractice(event, context):
    
    '''Initialize variables and ask the first question.  Also states the outcome
    of the previous game if this isn't the first game in the Alexa session.'''
    
    #Check how many question have been asked already in this game
    numTotal = event['session']['attributes']['numTotal']
    
    #If the user restarts the game, state their previous score and restart
    if numTotal > 0:
        
        #Preface the output string with the user's previous score
        numRight = event['session']['attributes']['numRight']
        outStr = 'You got {0} out of {1} right that time.  Starting a new game. '.format(numRight, numTotal)
        
    #If it's a new game with no previous questions, just say that we're starting a new game
    else:
        
        outStr = 'Starting a new game. '
    
    #Generate the next question and get all of the pertinent info surrounding it
    correctAnswer, questionStr, firstNum, mathType, secondNum = getMathQuestion(0,12,['plus','minus'])
    
    #Build the output text string for Alexa to say
    outStr = outStr + '\n' + questionStr
    outCardStr = outStr.replace('plus', '+').replace('minus','-').replace('times','x')
    
    #Python dictionary with the response information.  Keep the session alive.
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "numRight": 0,
            "numTotal": 0,
            "firstNum": firstNum,
            "secondNum": secondNum,
            "correctAnswer": correctAnswer,
            "mathType": mathType
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": outStr,
            },
            "card": {
                "type": "Simple",
                "title": "Math Practice",
                "content": outCardStr
            },
            "reprompt": {
                "outputSpeech": {
                "type": "PlainText",
                "text": "I'll repeat the question. {0}".format(questionStr)
                },
            },
            "shouldEndSession": 'false'
        }
    }
    return response
    
def mathPractice_repeatQuestion(event, context):
    
    '''Repeat the previous response'''
    
    numRight = event['session']['attributes']['numRight']
    numTotal = event['session']['attributes']['numTotal']
    mathType = event['session']['attributes']['mathType']
    firstNum = event['session']['attributes']['firstNum']
    secondNum = event['session']['attributes']['secondNum']
    correctAnswer = event['session']['attributes']['correctAnswer']
    
    #Repeat the previous question
    outStr = "I'll repeat the question.\n{0} {1} {2}".format(firstNum, mathType, secondNum)
    outCardStr = outStr.replace('plus', '+').replace('minus','-').replace('times','x')
    
    #Python dictionary with the response information.  Keep the session alive.
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "numRight": numRight,
            "numTotal": numTotal,
            "firstNum": firstNum,
            "secondNum": secondNum,
            "correctAnswer": correctAnswer,
            "mathType": mathType
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": outStr,
            },
            "card": {
                "type": "Simple",
                "title": "Math Practice",
                "content": outCardStr
            },
            "reprompt": {
                "outputSpeech": {
                "type": "PlainText",
                "text": "I'll repeat the question. {0}".format(outStr)
                },
            },
            "shouldEndSession": 'false'
        }
    }
    return response
    
def mathPractice_gotAnswer(event, context):
    
    '''Handles the user's input answer, updates the score, and serves up the
    next question.'''
    
    #Make sure that an actual game is in progress first.  If not, let the user
    #know that a game hasn't started yet.
    try:
        correctAnswer = event['session']['attributes']['correctAnswer']
    except:
        outStr = "<speak>Hey, we haven't even started yet! Say the word " + \
        "<break time='200ms'/>ready<break time='200ms'/> to start the " + \
        "game, the word <break time='250ms'/>restart<break time='250ms'/> " + \
        "to restart a game, and the word " + \
        "<break time='200ms'/>done<break time='200ms'/> or " + \
        "<break time='200ms'/>stop<break time='200ms'/> to stop the game.</speak>"
        
        outCardStr = "Hey, we haven't even started yet! Say the word " + \
        "ready to start the game, the word restart " + \
        "to restart a game, and the word done or " + \
        "stop to stop the game."
        
        #Python dictionary with the response information.  Keep the session alive.
        response = {
            "version": "1.0",
            "sessionAttributes": {
                "numRight": 0,
                "numTotal": 0
            },
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": outStr
                },
                "card": {
                    "type": "Simple",
                    "title": "Math Practice",
                    "content": outCardStr
                },
                "reprompt": {
                    "outputSpeech": {
                    "type": "PlainText",
                    "text": "Are you ready to begin?"
                    },
                },
                "shouldEndSession": 'false'
            }
        }
        return response
    
    #Get the user's numeric answer
    userAnswer = int(event['request']['intent']['slots']['answer']['value'])
    
    #See if the user said "negative" or "minus" before the answer.  Alexa
    #doesn't always handle negative numbers well, so we've got an extra {minus}
    #slot in the Alexa skill definition that can accept the values "minus" or
    #"negative".  If the user only said the number, then the 'value' key won't
    #exist in the event dictionary.
    try:
        minus = event['request']['intent']['slots']['minus']['value']
    except:
        minus = ''
        
    #Multiply the user's answer by -1 if necessary
    if minus in ['negative','minus']: userAnswer *= -1
    
    #Get the needed information to check the answer and update the score
    numRight = event['session']['attributes']['numRight']
    numTotal = event['session']['attributes']['numTotal']
    
    #Now actually check whether the user's right or not
    if userAnswer == correctAnswer:
        numRight += 1
        outStrStart = "That's correct! "
    else:
        outStrStart = "Sorry, the correct answer was {0}. ".format(correctAnswer)
    numTotal += 1
    
    #Generate the next question and get all of the pertinent info surrounding it
    correctAnswer, questionStr, firstNum, mathType, secondNum = getMathQuestion(0,12,['plus','minus'])
    
    #Generate Alexa's next statement
    outStr = outStrStart + '\n' + questionStr
    outCardStr = outStr.replace('plus', '+').replace('minus','-').replace('times','x')

    #Python dictionary with the response information.  Keep the session alive.
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "numRight": numRight,
            "numTotal": numTotal,
            "firstNum": firstNum,
            "secondNum": secondNum,
            "correctAnswer": correctAnswer,
            "mathType": mathType
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": outStr,
            },
            "card": {
                "type": "Simple",
                "title": "Math Practice",
                "content": outCardStr
            },
            "reprompt": {
                "outputSpeech": {
                "type": "PlainText",
                "text": "I'll repeat the question. {0}".format(questionStr)
                },
            },
            "shouldEndSession": 'false'
        }
    }
    return response
    
def mathPractice_endPractice(event, context):
    
    '''Ends the entire Alexa session, stating the final score for the current
    game.'''
    
    #Get the information needed to state the final score.
    numRight = event['session']['attributes']['numRight']
    numTotal = event['session']['attributes']['numTotal']
    
    #Generate Alexa's next statement.  If numTotal is zero, then there were no
    #actual questions asked in the final game, so just say goodbye.  Otherwise,
    #state the score for the final game.
    if numTotal == 0:
        outStr = 'Thanks for playing!'
    else:
        outStr = 'You got {0} out of {1} right. Thanks for playing!'.format(numRight, numTotal)
        
    outCardStr = outStr
    
    #Python dictionary with the response information.  End the session.
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": outStr
            },
            "card": {
                "type": "Simple",
                "title": "Math Practice",
                "content": outCardStr
            },
            "shouldEndSession": 'true'
        }
    }
    return response
    
def mathPractice_fallback(event, context):
    
    '''Fallback in case the user says something unexpected'''
    
    #Check whether a game has begun first.  If not, repeat the starting
    #instructions.  If so, restate the previous question.
    try:
        #If no session has begun yet, then there won't be any firstNum
        #attribute and we'll get sent to the except block.
        firstNum = event['session']['attributes']['firstNum']
        numRight = event['session']['attributes']['numRight']
        numTotal = event['session']['attributes']['numTotal']
        firstNum = event['session']['attributes']['firstNum']
        secondNum = event['session']['attributes']['secondNum']
        correctAnswer = int(event['session']['attributes']['correctAnswer'])
        mathType = event['session']['attributes']['mathType']
        
        #Tell the user that Alexa didn't understand and then restate the
        #current question
        outStr = "Sorry, I didn't understand your response.\n{0} {1} {2}".format(firstNum, mathType, secondNum)
        outCardStr = outStr
        
        #Python dictionary with the response information.  Keep the session alive.
        response = {
            "version": "1.0",
            "sessionAttributes": {
                "numRight": numRight,
                "numTotal": numTotal,
                "firstNum": firstNum,
                "secondNum": secondNum,
                "correctAnswer": correctAnswer,
                "mathType": mathType
            },
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": outStr
                },
                "card": {
                    "type": "Simple",
                    "title": "Math Practice",
                    "content": outCardStr
                },
                "shouldEndSession": 'false'
            }
        }
    except:
        #If we get here, then no session has begun yet, so just restate the
        #start, repeat, and end commands again
        outStr = "Sorry, I didn't understand your response. Say the word " + \
        "ready to start the game, the word restart to restart a game, and " + \
        "the word stop to stop the game."
        outCardStr = outStr
    
        #Python dictionary with the response information.  Keep the session alive.
        response = {
            "version": "1.0",
            "sessionAttributes": {
                "numRight": 0,
                "numTotal": 0
            },
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": outStr
                },
                "card": {
                    "type": "Simple",
                    "title": "Math Practice",
                    "content": outCardStr
                },
                "shouldEndSession": 'false'
            }
        }
    return response

def lambda_handler(event, context):

    print(event)
    
    #The user has just launched the skill
    if event['request']['type'] == "LaunchRequest":
        return mathPractice_launch(event, context)
        
    #The user is interacting with the skill post-launch
    if event['request']['type'] == "IntentRequest":
        print('got IntentRequest')
        print(event['request'])
        
        #The user is ready to start a new game
        if event['request']['intent']['name'] == "readyIntent":
            print('got readyIntent')
            return mathPractice_startPractice(event, context)
            
        #The user gives an answer
        if event['request']['intent']['name'] == "answerIntent":
            print('got answerIntent')
            return mathPractice_gotAnswer(event, context)
            
        #The user asks for the question to be repeated
        if event['request']['intent']['name'] == "repeatIntent":
            print('got repeatIntent')
            return mathPractice_repeatQuestion(event, context)
            
        #The user is done
        if event['request']['intent']['name'] == "AMAZON.StopIntent":
            print('got AMAZON.StopIntent')
            return mathPractice_endPractice(event, context)
            
        #Alexa didn't understand the user's request
        if event['request']['intent']['name'] == "AMAZON.FallbackIntent":
            print('got AMAZON.FallbackIntent')
            return mathPractice_fallback(event, context)