import { Component, useState } from '@odoo/owl';

export class Counter extends Component {
    static template = 'awesome_owl.counter';

    static props = {
        action: { type: String, optional: true },
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    notifyParent(newValue) {
        if (this.props.onChange) {
            this.props.onChange(newValue);
        }
    }

    increment() {
        this.state.value++;
        this.notifyParent(this.state.value);
    }

    decrement() {
        if (this.state.value > 0) {
            this.state.value--;
            this.notifyParent(this.state.value);
        }
    }
}
