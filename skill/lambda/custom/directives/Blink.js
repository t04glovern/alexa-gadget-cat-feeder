"use strict";

module.exports = {
    build: function (endpointId, intervalMs, iterations, startFeeder) {
        return {
            type: 'CustomInterfaceController.SendDirective',
            header: {
                name: 'Blink',
                namespace: 'Custom.CatFeederGadget'
            },
            endpoint: {
                endpointId: endpointId
            },
            payload: {
                intervalMs: intervalMs,
                iterations: iterations,
                startFeeder: startFeeder
            }
        };
    }
}