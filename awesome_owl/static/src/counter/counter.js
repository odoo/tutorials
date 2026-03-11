import { Component, useState } from "@odoo/owl";

export class Counter extends Component {

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        // notify parent if callback exists
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}

Counter.template = "awesome_owl.Counter";

/* Props validation */
Counter.props = {
    onChange: { type: Function, optional: true },
};
