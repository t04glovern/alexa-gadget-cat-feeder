"use strict";

const CleanupDirective = require('../directives/Cleanup');

module.exports = {
    canHandle(handlerInput) {
        let { request } = handlerInput.requestEnvelope;
        console.log("CustomEventHandler: checking if it can handle " + request.type);
        return request.type === 'CustomInterfaceController.Expired';
    },
    handle(handlerInput) {
        console.log("== Custom Event Expiration Input ==");

        let { request } = handlerInput.requestEnvelope;

        const attributesManager = handlerInput.attributesManager;
        let sessionAttributes = attributesManager.getSessionAttributes();

        // When the EventHandler expires, cleanup and close feeder
        return handlerInput.responseBuilder
            .addDirective(CleanupDirective.build(sessionAttributes.endpointId))
            .withShouldEndSession(true)
            .speak(request.expirationPayload.data)
            .getResponse();
    }
};