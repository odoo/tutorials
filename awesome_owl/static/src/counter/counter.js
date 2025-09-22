import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: Function
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        console.log("Incremented to", this.state.value);
        if ("onChange" in this.props) {
            console.log("Calling onChange callback");
            this.props.onChange();
        }
    }
}
