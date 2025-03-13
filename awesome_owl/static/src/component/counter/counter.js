/** @odoo-module **/

const { Component, useState } = owl;

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: {
            type: Function,
            optional: true
        }
    }

    setup() {
        this.state = useState({
            value: 0
        });
    }

    increment() {
        this.state.value ++;
        this.props.onChange?.();
    }
}
