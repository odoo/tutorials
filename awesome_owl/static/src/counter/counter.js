import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    update(val) {
        this.state.value += val;
        if (this.props.onChange) {
            this.props.onChange({
                value: this.state.value,
                operator: val,
            });
        }
    }
}
