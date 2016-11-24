from __future__ import print_function
import requests
import json

# --------------- Helpers that build all of the responses ----------------------
def getCGMValue():
    session_attributes = {}
    card_title = "Nightscout BG Value"
    reprompt_text = ""
    should_end_session = True
    
    nightscoutURL=  "YOUR NIGHTSCOUT URL HERE WITH HTTPS" + "/api/v1/entries/current.json"
    r=              requests.get(nightscoutURL)
    parsed=         r.json()
    currentValue=   parsed[0]['sgv']
    trendValue=     parsed[0]['direction']

    if trendValue == "Flat":
        direction = "stable"
    elif trendValue == "FourtyFiveUp":
        direction = "rising"
    elif trendValue == "SingleUp":
        direction = "rising quickly"
    elif trendValue == "FourtyFiveDown":
        direction = "Falling"
    elif trendValue == "DoubleUp":
        direction = "rising very quickly."
    elif trendValue == "SingleDown":
        direction = "Dropping quickly"
    elif trendValue == "DoubleDown":
        direction = "dropping very quickly!"
        
    speech_output = "Your most recent blood sugar value is " +str(currentValue)+ " and " + direction

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getCGMTrend():
    session_attributes = {}
    card_title = "Nightscout Trend Direction"
    reprompt_text = ""
    should_end_session = True
    
    nightscoutURL=  "YOUR NIGHTSCOUT URL HERE WITH HTTPS" + "/api/v1/entries/current.json"

    r=              requests.get(nightscoutURL)
    
    parsed=         r.json()
    trendValue=     parsed[0]['direction']

    if trendValue == "Flat":
        direction = "stable"
        speech_output = "Your blood sugar is currently stable."
    elif trendValue == "FourtyFiveUp":
        direction = "rising"
        speech_output = "Your blood sugar is rising slowly."
    elif trendValue == "SingleUp":
        direction = "rising quickly"
        speech_output = "Your blood sugar is rising quickly."
    elif trendValue == "FourtyFiveDown":
        direction = "Falling"
        speech_output = "Your blood sugar is falling slowly."
    elif trendValue == "DoubleUp":
        direction = "rising very quickly."
        speech_output = "Your blood sugar is rising very quickly."
    elif trendValue == "SingleDown":
        direction = "Dropping quickly"
        speech_output = "Your blood sugar is dropping quickly."
    elif trendValue == "DoubleDown":
        direction = "dropping very quickly!"
        speech_output = "Your blood sugar is dropping very quickly."
        print(speech_output)
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)) 


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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

def get_welcome_response():
    
    session_attributes = {}
    card_title = "Nightscout"
    speech_output = "Welcome to the unofficial Nightscout Skill for Amazon Echo. " \
                    "You can ask me what your current blood sugar value is, " \
                    "or how you are trending"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me what you current blood sugar is." 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Nighscout - Thanks!"
    speech_output = "Thanks for using the Nighscout skill " \
                    "Have a nice day and keep up the good work! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    print("Starting new session...")


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetBGValue":
        return getCGMValue()
    elif intent_name == "GetTrend":
        return getCGMTrend()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("Ending session")


# --------------- Main handler ------------------

def lambda_handler(event, context):
    def lambda_handler(event, context):
        if (event["session"]["application"]["applicationId"] !=
                "amzn1.ask.skill.ea32a28a-e0f6-440f-96ab-b6c12f717ed3"):
            raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
