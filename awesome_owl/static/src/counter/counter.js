/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter.counter";
    static props = {
        onChange: {
            type: Function,
            optional: true,
        },
        counter: Object
    }

    setup() {
    };

    updateValue(newValue) {
        this.props.counter.value = newValue;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }

    increment() {
        this.updateValue(this.props.counter.value + 1);
    }
    decrement() {
        this.updateValue(this.props.counter.value - 1);
    }
}