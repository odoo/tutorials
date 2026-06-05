import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        value: Number,
        onChange: { type: Function, optional: true }
    };

    increment() {
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
