const Alexa = require('ask-sdk-core');

// i18n library dependency, we use it below in a localisation interceptor
const i18n = require('i18next');

// i18n strings for all supported locales
const languageStrings = require('./languageStrings');

// Base Intent Handlers
const CancelAndStopIntentHandler = require('./intents/base/CancelAndStop');
const ErrorHandler = require('./intents/base/Error');
const FallbackIntentHandler = require('./intents/base/Fallback');
const HelpIntentHandler = require('./intents/base/Help');
const LaunchRequestHandler = require('./intents/base/Launch');
const SessionEndedRequestHandler = require('./intents/base/SessionEnd');

// Custom Intents
const YesIntentHandler = require('./intents/YesFeed');
const NoIntentHandler = require('./intents/NoFeed');
const ReportFeederIntentHandler = require('./intents/ReportFeeder');
const ExpiredFeederIntentHandler = require('./intents/ExpireFeeder');

// This request interceptor will bind a translation function 't' to the handlerInput
const LocalisationRequestInterceptor = {
    process(handlerInput) {
        i18n.init({
            lng: Alexa.getLocale(handlerInput.requestEnvelope),
            resources: languageStrings
        }).then((t) => {
            handlerInput.t = (...args) => t(...args);
        });
    }
};

const skillBuilder = Alexa.SkillBuilders.custom();
exports.handler = skillBuilder
    .addRequestHandlers(
        CancelAndStopIntentHandler, // Base Intents
        FallbackIntentHandler,
        HelpIntentHandler,
        LaunchRequestHandler,
        SessionEndedRequestHandler,
        YesIntentHandler,           // Custom Intents
        NoIntentHandler,
        ReportFeederIntentHandler,
        ExpiredFeederIntentHandler
    )
    .addErrorHandlers(
        ErrorHandler
    )
    .addRequestInterceptors(
        LocalisationRequestInterceptor
    )
    .withApiClient(new Alexa.DefaultApiClient())
    .lambda();
