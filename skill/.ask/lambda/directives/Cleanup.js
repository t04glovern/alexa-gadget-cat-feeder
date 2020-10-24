"use strict";

module.exports = {
    build: function (endpointId) {
        return {
            type: 'CustomInterfaceController.SendDirective',
            header: {
                name: 'Cleanup',
                namespace: 'Custom.CatFeederGadget'
            },
            endpoint: {
                endpointId: endpointId
            },
            payload: {}
        };
    }
}