import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    setup() {
        this.state = useState({
            count: 0
        });
    }

    increment() {
        this.state.count++;

        if (this.props.onChange) {
            this.props.onChange(this.state.count);
        }
    }

    decrement() {
        if (this.state.count>0){
            this.state.count--;

            if (this.props.onchanges) {
                this.props.onchanges(this.state.count);
            }
        }
    }
}