/* eslint-disable  func-names */
/* eslint-disable  no-console */

const Alexa = require('ask-sdk-core');
const Xray = require('x-ray');
const moment = require('moment');
let x = Xray();

const LaunchRequest = {
  canHandle(handlerInput) {
    const { request } = handlerInput.requestEnvelope;

    return request.type === 'LaunchRequest'
      || (request.type === 'IntentRequest'
        && request.intent.name === 'AMAZON.StartOverIntent');
  },
  handle(handlerInput) {
    return handlerInput.responseBuilder
      .speak('Willkommen bei Delzepich. Frag mich einfach, nach den Eissorten für einen bestimmten Tag.')
        .getResponse();
  },
};

const StopIntent = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent' || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent');
  },
  handle(handlerInput) {

    return handlerInput.responseBuilder
      .speak('Ok bis dann')
      .getResponse();
  },
};

let getIcecreamsOfDDate = function(date){
  let promise = new Promise(function(resolve, reject){
    x('https://www.delzepicheis.de/',{
    dates: x('.tag-inner', [
      {
        dateStr: 'span.datum',
        types: ['ul.tags li']
    }])
  })(function(err, res){
    let matchingDate = res.dates.filter(d => d.dateStr === moment(date).format('DD.MM.YYYY'))
    if( matchingDate && err === null) {
      resolve(matchingDate[0].types);
    } else {
      reject(err);
    }
  });
  });

  return promise;

}

const ErrorHandler = {
  canHandle() {
    return true;
  },
  handle(handlerInput, error) {
    console.log(`Error handled: ${error.message}`);

    return handlerInput.responseBuilder
      .speak('Entschuldige, das habe ich nicht verstanden, bitte versuch es nochmal.')
      .reprompt('Entschuldige, das habe ich nicht verstanden, bitte versuch es nochmal.')
      .getResponse(); 
  },
};

const IcecreamIntent = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'IcecreamIntent';
  },
  handle(handlerInput) {
    const requestAttributes = handlerInput.attributesManager.getRequestAttributes();

    getIcecreamsOfDDate(requestAttributes[0]).then(function(types){

      if(types && types.length) {
        return handlerInput.responseBuilder.speak('Die Eissorten sind für den '+requestAttributes[0]+': '+types.join(','))
        .getResponse();

      } else {
        return handlerInput.responseBuilder.speak('Für den '+requestAttributes[0]+' habe ich leider keine Eissorten gefunden')
        .getResponse();

      }

    }).catch(function(error) {
      return handlerInput.responseBuilder.speak('Leider ist ein Fehler aufgetreten');
    });
  },
};

const skillBuilder = Alexa.SkillBuilders.custom();
exports.handler = skillBuilder
  .addRequestHandlers(
    LaunchRequest,
    StopIntent,
    IcecreamIntent
  )
  .addErrorHandlers(ErrorHandler)
  .lambda();
