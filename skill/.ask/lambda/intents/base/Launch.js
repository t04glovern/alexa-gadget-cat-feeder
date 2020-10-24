"use strict";

const InitDirective = require('../../directives/Init');

module.exports = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    async handle(handlerInput) {
        let response;
        try {
            // Get connected gadget endpointId.
            console.log("Checking endpoint");
            response = await getConnectedEndpointsResponse(handlerInput);
            console.log("v1/endpoints response: " + JSON.stringify(response));

            if ((response.endpoints || []).length === 0) {
                console.log('No connected gadget endpoints available');
                response = handlerInput.responseBuilder
                    .speak("No gadgets found. Please try again after connecting your gadget.")
                    .getResponse();
                return response;
            }

            let endpointId = response.endpoints[0].endpointId;

            // Store endpointId for using it to send custom directives later.
            console.log("Received endpoints. Storing Endpoint Id: " + endpointId);
            const attributesManager = handlerInput.attributesManager;
            let sessionAttributes = attributesManager.getSessionAttributes();
            sessionAttributes.endpointId = endpointId;
            attributesManager.setSessionAttributes(sessionAttributes);

            return handlerInput.responseBuilder
                .speak(handlerInput.t('WELCOME_MSG'))
                .withShouldEndSession(false)
                // Send the init directive
                .addDirective(InitDirective.build(endpointId))
                .getResponse();
        }
        catch (err) {
            console.log("An error occurred while getting endpoints", err);
            response = handlerInput.responseBuilder
                .speak("I wasn't able to get connected endpoints. Please try again.")
                .withShouldEndSession(true)
                .getResponse();
            return response;
        }
    }
}

function getConnectedEndpointsResponse(handlerInput) {
    return handlerInput.serviceClientFactory.getEndpointEnumerationServiceClient().getEndpoints();
}