/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = ['onChange?'];
    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if(this.props.onChange){
            this.props.onChange();
        }
    }
}