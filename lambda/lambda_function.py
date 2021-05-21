import datetime
import logging

import requests
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from bs4 import BeautifulSoup

skill_name = "Delzepich Eis"
help_text = "Ich kann dir die Eissorten von Delzepich verraten"
date_text = "Von welchem Tag willst du die Sorten hören?"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech = "Hallo bei Delzepich eis, von welchem Tag willst du die Eissorten hören"

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
        speech = "die heutigen Eissorten sind: " + ','.join(get_icecreams_of_date(parsed_date))
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
    r = requests.get(url='https://apps.wixrestaurants.com/?type=wixmenus.client&pageId=v5j7g&compId=TPASection_kd8szihu&viewerCompId=TPASection_kd8szihu&siteRevision=646&viewMode=site&deviceType=desktop&locale=de&tz=Europe%2FBerlin&regionalLanguage=de&width=643&height=2418&instance=8U0BgGkq-yhBaHR9Chjk6dvGlx457Izw1CBIMiRZkRE.eyJpbnN0YW5jZUlkIjoiZDUyYTNmZDAtZmE3Ny00YTc3LWI5ZWItMTQzM2NiOGU5ZTFmIiwiYXBwRGVmSWQiOiIxM2MxNDAyYy0yN2YyLWQ0YWItNzQ2My1lZTdjODllMDc1NzgiLCJtZXRhU2l0ZUlkIjoiY2ViMDdhYWUtYTQ5Yi00NzgwLWIyYzUtZDFhNmZiNmEwOGMzIiwic2lnbkRhdGUiOiIyMDIxLTA1LTIxVDA5OjIzOjM4Ljc0M1oiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJyZXN0X3BybyIsImRlbW9Nb2RlIjpmYWxzZSwiYWlkIjoiYTRjNDE4NzgtM2E0Ny00ZThmLTk5ZDktYzc3NDdkYjVlODUwIiwiYmlUb2tlbiI6IjFiOWE0NTdlLTVlZWMtMGRmNy0wYjJlLWM1OTUzMGU0OTZkYyIsInNpdGVPd25lcklkIjoiNGU0OTlmNTctOGU3My00MGRhLTg0MmUtYzY3N2U0Yjg2MGJhIn0&currency=EUR&currentCurrency=EUR&commonConfig=%7B%22brand%22%3A%22wix%22%2C%22bsi%22%3A%2295342bf5-132f-45cc-bc38-0565d6e44ba2%7C2%22%2C%22BSI%22%3A%2295342bf5-132f-45cc-bc38-0565d6e44ba2%7C2%22%7D&target=_top&section-url=https%3A%2F%2Fwww.delzepicheis.de%2Fmenus%2F&vsi=e7f8d12e-a966-426d-aa79-0868ae7f3c3c')
    soup = BeautifulSoup(r.text, 'html.parser')
    requested_day_div = [day for day in soup.findAll("div", {"class": "yummyMsw8T"}) if
                          day.string == date.strftime('%d.%m.%Y')]

    if requested_day_div:
        variations = requested_day_div[0].parent.next_sibling.contents
        return [variaton.text for variaton in variations if variaton != '']
    return []


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()
