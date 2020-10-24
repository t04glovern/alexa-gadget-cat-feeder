"use strict";

const CleanupDirective = require('../directives/Cleanup');

module.exports = {
    canHandle(handlerInput) {
        let { request } = handlerInput.requestEnvelope;
        console.log("CustomEventHandler: checking if it can handle " + request.type);
        return request.type === 'CustomInterfaceController.EventsReceived';
    },
    handle(handlerInput) {
        console.log("== Received Custom Event ==");

        let { request } = handlerInput.requestEnvelope;

        const attributesManager = handlerInput.attributesManager;
        let sessionAttributes = attributesManager.getSessionAttributes();

        // Validate eventHandler token
        if (sessionAttributes.token !== request.token) {
            console.log("EventHandler token doesn't match. Ignoring this event.");
            return handlerInput.responseBuilder
                .speak("EventHandler token doesn't match. Ignoring this event.")
                .getResponse();
        }

        let customEvent = request.events[0];
        let payload = customEvent.payload;
        let namespace = customEvent.header.namespace;
        let name = customEvent.header.name;

        let response = handlerInput.responseBuilder;

        if (namespace === 'Custom.CatFeederGadget' && name === 'ReportFeeder') {
            // On receipt of 'Custom.CatFeederGadget.ReportFeeder' event, check success
            // then end the skill session
            if (payload.feed) {
                return response.speak('Cat has been fed, Meow!')
                    .addDirective(CleanupDirective.build(sessionAttributes.endpointId))
                    .withShouldEndSession(true)
                    .getResponse();
            } else {
                return response.speak('Feeder encountered an error responding. Check the gadget device and I/O')
                    .addDirective(CleanupDirective.build(sessionAttributes.endpointId))
                    .withShouldEndSession(true)
                    .getResponse();
            }

        }
        return response;
    }
};