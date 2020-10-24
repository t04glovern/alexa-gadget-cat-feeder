"use strict";

const Uuid = require('uuid/v4');

const FeedCatDirective = require('../directives/FeedCat');
const StartEventHandlerDirective = require('../directives/StartEventHandler');

module.exports = {
    canHandle(handlerInput) {
        let { request } = handlerInput.requestEnvelope;
        let intentName = request.intent ? request.intent.name : '';
        console.log("YesIntentHandler: checking if it can handle " +
            request.type + " for " + intentName);
        return request.intent && request.intent.name === 'AMAZON.YesIntent';
    },
    handle(handlerInput) {
        // Retrieve the stored gadget endpointId from the SessionAttributes.
        const attributesManager = handlerInput.attributesManager;
        let sessionAttributes = attributesManager.getSessionAttributes();
        let endpointId = sessionAttributes.endpointId;

        // Create a token to be assigned to the EventHandler and store it
        // in session attributes for stopping the EventHandler later.
        sessionAttributes.token = Uuid();
        attributesManager.setSessionAttributes(sessionAttributes);

        console.log("YesIntent received. Starting feeder.");

        return handlerInput.responseBuilder
            // Send the FeedCatDirective to trigger the feeder.
            .addDirective(FeedCatDirective.build(endpointId))
            // Start a EventHandler for 10 seconds to receive only one
            // 'Custom.CatFeederGadget.ReportFeeder' event and terminate.
            .addDirective(StartEventHandlerDirective.build(sessionAttributes.token, 10000,
                'Custom.CatFeederGadget', 'ReportFeeder', 'SEND_AND_TERMINATE',
                { 'data': "You didn't report a feed took place. Good bye!" }))
            .getResponse();
    }
};