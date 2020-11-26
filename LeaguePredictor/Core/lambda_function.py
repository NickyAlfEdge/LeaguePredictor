import tool_functions
import predict_outcome
import boto3

# dynamodb init connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Account')


# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_account_name_response(intent, session):
    card_title = "User"
    attributes = session.get('attributes', {})
    previous_intent = attributes['previous_intent']
    if previous_intent == 'welcome_new_account' or previous_intent == 'add_account':
        ask_id = session["user"]["userId"]
        user = tool_functions.parse_id(ask_id)
        intent_slots = intent['slots']
        account_name = tool_functions.format_account_name(intent_slots)
        if 'Account Length Error' in account_name:
            session_attributes = {"previous_intent": "account_error"}
            speech_output = "The account name, {} is too long. League of Legends accounts should range from 3 to 16 characters in length. Would you like to try again?".format(account_name)
            reprompt_text = "There was an error with your account name, would you like to try again?"
            should_end_session = False
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            session_attributes = {"previous_intent": "new_account"}
            table.put_item(Item={'AccountID': user, 'AccountName': account_name})
            split_name = tool_functions.split_name(account_name)
            speech_output = "You said, {} is this correct? Please state yes or no to continue.".format(split_name)
            reprompt_text = "Is the account name {} correct?".format(account_name)
            should_end_session = False
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))


def get_game_outcome_response(session):
    card_title = "Predict Winner"
    attributes = session.get('attributes', {})
    previous_intent = attributes['previous_intent']
    if previous_intent == "begin_prediction":
        session_attributes = {"previous_intent": "prediction"}
        ask_id = session["user"]["userId"]
        user = tool_functions.parse_id(ask_id)
        db_item = tool_functions.in_database(user)
        account_name = db_item['AccountName']
        match_data = predict_outcome.load_match_data(account_name)
        if "Error" in match_data:
            speech_output = "A live match could not be found for {} Please ensure you're in a game of classic summoners rift 5 vs 5 prior to running this tool again.".format(account_name)
            reprompt_text = ""
            should_end_session = True
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            result = predict_outcome.prediction(match_data)
            speech_output = result
            reprompt_text = ""
            should_end_session = True
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))


def get_yes_response(session):
    card_title = "Yes"
    attributes = session.get('attributes', {})
    previous_intent = attributes['previous_intent']
    if previous_intent == "welcome_old_account" or previous_intent == "new_account":
        session_attributes = {"previous_intent": "validate_game_status"}
        ask_id = session["user"]["userId"]
        user = tool_functions.parse_id(ask_id)
        db_item = tool_functions.in_database(user)
        account_name = db_item['AccountName']
        match_status = predict_outcome.get_match_status(account_name)
        if match_status is not None:
            speech_output = "Please ensure you are in a game, or supplying a valid account within the Europe West region for this tool to function correctly. Goodbye."
            reprompt_text = ""
            should_end_session = True
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            speech_output = "Okay, great, initial validation has been carried out and we are ready to begin predicting your game. Would you like to continue?"
            reprompt_text = ""
            should_end_session = False
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    elif previous_intent == "add_account" or previous_intent == "welcome_new_account":
        session_attributes = {"previous_intent": "add_account"}
        speech_output = "Sorry, but when providing your account name, can you ensure you are only spelling it out character by character. Please try again."
        reprompt_text = ""
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    elif previous_intent == "account_error":
        session_attributes = {"previous_intent": "add_account"}
        speech_output = "Okay. Please spell your account name character by character, saying space where there are spaces within your account name."
        reprompt_text = ""
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    elif previous_intent == "validate_game_status":
        session_attributes = {"previous_intent": "begin_prediction"}
        speech_output = "Great, please say predict my match, for the process to begin. Good luck!"
        reprompt_text = ""
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def get_no_response(session):
    card_title = "No"
    attributes = session.get('attributes', {})
    previous_intent = attributes['previous_intent']
    if previous_intent == "welcome_old_account" or previous_intent == "new_account":
        ask_id = session["user"]["userId"]
        user = tool_functions.parse_id(ask_id)
        table.delete_item(Key={'AccountID': user})
        session_attributes = {"previous_intent": "add_account"}
        speech_output = "Okay. Please spell your account name character by character, saying space where there are spaces within your account name."
        reprompt_text = ""
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    elif previous_intent == "add_account":
        session_attributes = {"previous_intent": "add_account"}
        speech_output = "Alright, thank you for using the League of Legends match predictor. Have a great day."
        reprompt_text = ""
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    elif previous_intent == "validate_game_status" or previous_intent == "account_error" or previous_intent == "begin_prediction":
        return handle_session_end_request()


def get_welcome_response(session):
    card_title = "Welcome"
    ask_id = session["user"]["userId"]
    user = tool_functions.parse_id(ask_id)
    db_item = tool_functions.in_database(user)
    if db_item is None:
        session_attributes = {"previous_intent": "welcome_new_account"}
        speech_output = "Welcome to the League of Legends match prediction skill, please spell out your account name for a prediction to be made. Spaces can be entered through saying space."
        reprompt_text = "Please spell out your account name for a prediction to be made. Spaces can be entered through saying space."
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    else:
        session_attributes = {"previous_intent": "welcome_old_account"}
        account_name = db_item['AccountName']
        speech_output = "Welcome to the League of Legends match prediction skill. Account {} was found for your account, would you like to continue with this account?".format(account_name)
        reprompt_text = "Would you like to predict a games outcome for the account {}?".format(account_name)
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the League of Legends Match Predictor. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    # Dispatch to your skill's launch message
    return get_welcome_response(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to  skill's intent handlers
    if intent_name == "AccountNameIntent":
        return get_account_name_response(intent, session)
    if intent_name == "PredictOutcomeIntent":
        return get_game_outcome_response(session)
    if intent_name == "AMAZON.YesIntent":
        return get_yes_response(session)
    if intent_name == "AMAZON.NoIntent":
        return get_no_response(session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Used for tracking"""
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
