"use strict";

module.exports = {
    build: function (endpointId) {
        return {
            type: 'CustomInterfaceController.SendDirective',
            header: {
                name: 'FeedCat',
                namespace: 'Custom.CatFeederGadget'
            },
            endpoint: {
                endpointId: endpointId
            },
            payload: {}
        };
    }
}