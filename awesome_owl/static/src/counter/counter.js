import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter"
    static props = {
        callback: {
            type: Function,
            optional: true
        }
    }

    setup() {
        this.state = useState({ val: 0 })
    }

    increment() {
        this.state.val++;
        if (this.props.callback) {
            this.props.callback()
        }
    }
}
