import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: { type: Function, optional: true } 
    };

    setup() {
        this.state = useState({ counterValue: 0 });
    }

    increment() {
        this.state.counterValue++;
        this.notifyParent(1);
    }

    decrement() {
        this.state.counterValue--;
        this.notifyParent(-1);
    }
    
    notifyParent(delta) {
        if (this.props.onChange) {
            this.props.onChange(delta);
        }
    }
}
