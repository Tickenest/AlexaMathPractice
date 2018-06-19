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
    
    outStr = "I'll tell you a math question. Don't say Alexa, just say your answer. " + \
            "I'll tell you if you're right or wrong, and then give you another question. " + \
            "Say the word ready to start the session, the word restart to restart the " + \
            "session, and the word done to end the session."

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
    outStr = outStr + questionStr
    
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
    correctAnswer = int(event['session']['attributes']['correctAnswer'])
    
    #Repeat the previous question
    outStr = "I'll repeat the question. {0} {1} {2}".format(firstNum, mathType, secondNum)
    
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
            "shouldEndSession": 'false'
        }
    }
    return response
    
def mathPractice_gotAnswer(event, context):
    
    '''Handles the user's input answer, updates the score, and serves up the
    next question.'''
    
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
    correctAnswer = int(event['session']['attributes']['correctAnswer'])
    
    #Now actually check whether the user's right or not
    if userAnswer == correctAnswer:
        numRight += 1
        outStrStart = "That's correct! "
    else:
        outStrStart = "Sorry, the correct answer was {0}. ".format(correctAnswer)
    numTotal += 1
    
    #Generate the next question and get all of the pertinent info surrounding it
    correctAnswer, outStr, firstNum, mathType, secondNum = getMathQuestion(0,12,['plus','minus'])
    
    #Generate Alexa's next statement
    outStr = outStrStart + outStr

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
    
    #Python dictionary with the response information.  End the session.
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": outStr
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
        outStr = "Sorry, I didn't understand your response. {0} {1} {2}".format(firstNum, mathType, secondNum)
        
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
                "shouldEndSession": 'false'
            }
        }
    except:
        #If we get here, then no session has begun yet, so just restate the
        #start, repeat, and end commands again
        outStr = "Sorry, I didn't understand your response. Say the word " + \
        "ready to start the game, the word restart to restart a game, and " + \
        "the word stop to stop the game."
    
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
                "shouldEndSession": 'false'
            }
        }
    return response

def lambda_handler(event, context):

    print(event)
    
    if event['request']['type'] == "LaunchRequest":
        return mathPractice_launch(event, context)
        
    if event['request']['type'] == "IntentRequest":
        print('got IntentRequest')
        print(event['request'])
        
        if event['request']['intent']['name'] == "readyIntent":
            print('got readyIntent')
            return mathPractice_startPractice(event, context)
            
        if event['request']['intent']['name'] == "answerIntent":
            print('got answerIntent')
            return mathPractice_gotAnswer(event, context)
            
        if event['request']['intent']['name'] == "repeatIntent":
            print('got repeatIntent')
            return mathPractice_repeatQuestion(event, context)
            
        if event['request']['intent']['name'] == "AMAZON.StopIntent":
            print('got AMAZON.StopIntent')
            return mathPractice_endPractice(event, context)
            
        if event['request']['intent']['name'] == "AMAZON.FallbackIntent":
            print('got AMAZON.FallbackIntent')
            return mathPractice_fallback(event, context)