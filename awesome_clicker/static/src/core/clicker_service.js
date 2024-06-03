/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Reactive } from "@web/core/utils/reactive";

class ClickerStore extends Reactive {
    constructor() {
        super();
        this.setup(...arguments);
    }

    setup() {
        this.counter = 0;
    }

    increment(amount = 1) {
        this.counter += amount;
    }
}

const clickerService = {
    start(env, dependencies) {
        return new ClickerStore(env, dependencies);
    }
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
