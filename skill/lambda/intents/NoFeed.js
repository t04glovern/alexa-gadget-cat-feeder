"use strict";

const CleanupDirective = require('../directives/Cleanup');

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

        // Send Cleanup directive to cleanup I/O end skill session.
        return handlerInput.responseBuilder
            .addDirective(CleanupDirective.build(sessionAttributes.endpointId))
            .speak("Alright. Good bye!")
            .withShouldEndSession(true)
            .getResponse();
    }
};