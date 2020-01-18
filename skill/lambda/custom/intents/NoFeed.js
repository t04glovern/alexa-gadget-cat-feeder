"use strict";

const StopBlinkDirective = require('../directives/StopBlink');

module.exports = {
    canHandle(handlerInput) {
        let { request } = handlerInput.requestEnvelope;
        let intentName = request.intent ? request.intent.name : '';
        console.log("NoIntentHandler: checking if it can handle " +
            request.type + " for " + intentName);
        return request.intent && request.intent.name === 'AMAZON.NoIntent';
    },
    handle(handlerInput) {
        console.log("Received NoIntent..Exiting.");
        const attributesManager = handlerInput.attributesManager;
        let sessionAttributes = attributesManager.getSessionAttributes();

        // Send StopBlink directive to stop LED animation and end skill session.
        return handlerInput.responseBuilder
            .addDirective(StopBlinkDirective.build(sessionAttributes.endpointId))
            .speak("Alright. Good bye!")
            .withShouldEndSession(true)
            .getResponse();
    }
};