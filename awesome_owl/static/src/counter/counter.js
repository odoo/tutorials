import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = { 
        value: {optional: true},
        side_effect: {type: Function, optional: true}
    }

    setup() {
        this.state = useState({ value: this.props.value || 0});
    }

    increment() {
        this.props.side_effect ? this.props.side_effect() : true;
        this.state.value++;
    }
}
