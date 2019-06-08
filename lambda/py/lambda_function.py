import datetime
import logging
import sys

import requests
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from bs4 import BeautifulSoup

skill_name = "Delzepich Eis"
help_text = ("Ich kann dir die Eissorten von Delzepich verraten")
date_text = ("Von welchem Tag willst du die Sorten hören?")

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech = "Hallo bei Delzepich eis, von welchem Tag willst du die Einssorten hören"

    handler_input.response_builder.ask(speech)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    handler_input.response_builder.speak(help_text).ask(date_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
    is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("IcecreamIntent"))
def icecream_handler(handler_input):
    """
    Handler for date based icecream intent
    :param handler_input:
    :return:
    """
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots

    if 'date' in slots:
        date = slots['date'].value
        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        speech = "die heutigen Eissorten sind: "+','.join(get_icecreams_of_date(parsed_date))
    else:
        speech = "Das habe ich leider nicht verstanden"

    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response

@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))

    speech = "Da ist etwas schief gegangen, probiers nochmal"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response

def get_icecreams_of_date(date):
    r = requests.get(url = 'https://www.delzepicheis.de/')
    soup = BeautifulSoup(r.text, 'html.parser')
    requested_day_span = [day for day in soup.findAll("span", {"class": "datum"}) if day.string == date.strftime('%d.%m.%Y')]

    if requested_day_span:
        types = requested_day_span[0].parent.parent.contents[3].text.split('\n')
        return [type for type in types if type != '']
    return []

# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()