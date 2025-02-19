import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onchange: Function
    }

    setup() {
        this.count = useState({ value: 1 });
        
    }

    increment() {
        this.count.value++;
        if(this.props.onchange())
            this.props.onchange();
    }
}
