/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        onChange: {type: Function, optional: true}
    }

    setup() {
        this.state = useState({ value: 1 });
    }

    increment(e) {
        e.stopPropagation();
        this.state.value++;

        this.props.onChange && this.props.onChange();
    }
}

