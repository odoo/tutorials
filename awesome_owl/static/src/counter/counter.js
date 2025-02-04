import { useState, Component } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 1 });
    }

    increment=() =>{
        this.state.value++;
        this.props.incrementsum()
    }
}
