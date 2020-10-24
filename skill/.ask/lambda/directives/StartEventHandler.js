"use strict";

module.exports = {
    build: function (token, durationMs, namespace, name, filterMatchAction, expirationPayload) {
        return {
            type: "CustomInterfaceController.StartEventHandler",
            token: token,
            eventFilter: {
                filterExpression: {
                    'and': [
                        { '==': [{ 'var': 'header.namespace' }, namespace] },
                        { '==': [{ 'var': 'header.name' }, name] }
                    ]
                },
                filterMatchAction: filterMatchAction
            },
            expiration: {
                durationInMilliseconds: durationMs,
                expirationPayload: expirationPayload
            }
        };
    }
}