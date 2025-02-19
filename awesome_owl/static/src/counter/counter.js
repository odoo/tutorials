import { useState, Component } from "@odoo/owl"

export class Counter extends Component{
    static template = "awesome_owl.counter_template"
    static props = {
        onChange: {type: Function, optional:false}
    }
    state = useState({ value: 0 });

    increment() {
        this.state.value++;
        this.props.onChange(1);
    }
}
