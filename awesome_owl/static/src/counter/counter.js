/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        onChange: {type: Function, optional: true},
    };

    count = useState({ value: 0 });

    increment() {
        this.count.value++;
        if (this.props.onChange) {
            this.props.onChange()
        }
    }
}
