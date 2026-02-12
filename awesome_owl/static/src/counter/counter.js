/** @odoo-module **/
import { Component, useState} from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        onChange: { type: Function, optional: true },
        };

    setup() {
        this.state = useState({ counter: 0 });
//        debugger;
    }

    increment() {
        this.state.counter += 1;
        if (this.props.onChange) {
            this.props.onChange(this.state.counter);
        }
    }
}
//Counter.template = "awesome_owl.Counter";
