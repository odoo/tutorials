import {Component, useState} from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        description: {type: String, optional: true},
        onChange: {type: Function, optional: true},
    }

    setup() {
        super.setup();

        this.state = useState({
            counter: 0,
        });
    }

    increment() {
        this.state.counter++;

        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
