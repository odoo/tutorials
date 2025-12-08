/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        callback: {
            type: Function,
            optional: true,
        }
    }

    setup() {
        this.count = useState({ value: 0 });
    }

    increment() {
        this.count.value += 1;
        this.props.callback?.();
    }
}
