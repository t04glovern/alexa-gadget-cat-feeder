"use strict";

const StopFeederDirective = require('../../directives/StopFeeder');

module.exports = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
                || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        console.log("Received a Stop or a Cancel Intent..");

        let { attributesManager, responseBuilder } = handlerInput;
        let sessionAttributes = attributesManager.getSessionAttributes();

        // When the user stops the skill, stop the EventHandler,
        // send StopFeeder directive to stop the skill session.
        if (sessionAttributes.token) {
            console.log("Active session detected, sending stop EventHandlerDirective.");
            responseBuilder.addDirective(StopFeederDirective.build(sessionAttributes.token));
        }

        const speakOutput = handlerInput.t('GOODBYE_MSG');
        return responseBuilder.speak(speakOutput)
            .addDirective(buildStopLEDDirective(sessionAttributes.endpointId))
            .withShouldEndSession(true)
            .getResponse();
    }
}