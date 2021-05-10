import dialogflow_v2 as dialogflow
import os
from gnewsclient import gnewsclient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-sxkp"

client = gnewsclient.NewsClient()   # Creating a gnews client this will hepl me in getting the news.


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result


def get_reply(query, chat_id):
    print(f'xxxx{query}')
    # Getting the type of intent the message is
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':    # If it is of get_news then we display the news
        # We say that the msg was get_news and we return the parameter i.e. topic,location,language
        return "get_news", dict(response.parameters)
    else:   # Else we give a pre defined reply to some of the question ans say that the msg is of small_talk
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
    # Setting the language parameter as the language in which we want the news
    client.language = parameters.get('language')
    # Setting the country news we want
    client.location = parameters.get('geo-country')
    # Setting the topic of the news we want
    client.topic = parameters.get('topic')
    # Getting the 1st five news that satisfy all the criteria
    return client.get_news()[:5]

topics_keyboard = [
    ['Health', 'World', 'Nation'], 
    ['Buisness', 'Technology', 'Entertainment'], 
    ['Sport', 'Science', 'Food']
]
