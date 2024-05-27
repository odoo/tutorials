/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter"

    setup() {
        this.state = useState({
            counter: 0,
        });
    }

    increment() {
        this.state.counter++;
        if(this.props.onChange) {
            this.props.onChange();
        }
    }
}