/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 100000);
    },
};

registry.category("services").add("myService", myService);

const sharedStateService = {
    start(env) {
        let state = {};
        return {
            getValue(key) {
                return state[key];
            },
            setValue(key, value) {
                state[key] = value;
            },
        };
    },
};

registry.category("services").add("shared_state", sharedStateService);

import { useService } from "@web/core/utils/hooks";

export class PrintComponent extends Component {
    setup() {
        this.sharedState = useService("shared_state");
        this.sharedState.setValue("somekey1", "somevalue1");
        const value = this.sharedState.getValue("somekey1");
        console.log("Value is ", value);
    }
}
