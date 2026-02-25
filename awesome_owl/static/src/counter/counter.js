import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        callback: {
            type: Function,
            optional: true,
        }
    }

    setup() {
        super.setup();

        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        if (this.props.callback) {
            this.props.callback(this.state.value);
        }
    }


}