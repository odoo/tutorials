import { Component, useState } from "@odoo/owl";


export class Counter extends Component {
    static template = "awesome_owl.counter";
    static prop = {
        onChange : {
            type: Function
        },
    }

    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
        if(this.props.onChange) {
            this.props.onChange(1);
        }
    }
}
