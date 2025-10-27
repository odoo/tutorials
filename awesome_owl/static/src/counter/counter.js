import {Component, useState} from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter"
    state = useState({value: 1})
    static props = {
        onChange: { typ: Function, optional: true }
    }

    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}