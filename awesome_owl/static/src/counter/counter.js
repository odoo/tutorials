import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        value: {type: Number, optional: true},
        onIncrement: {type: Function, optional: true},
    };

    // increment() {
    //     this.props.onIncrement();
    // }
}