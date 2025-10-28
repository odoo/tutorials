import { Component, useState } from "@odoo/owl"


export class Counter extends Component {
    static template = "awesome_owl.counter.counter"
    static props = ['onchange?']

    setup() {
        this.counter = useState({ value: 0 });
    }

    increment() {
        this.counter.value++;
        if(this.props.onchange != null && this.props.onchange != undefined)
            this.props.onchange()
    }
}
