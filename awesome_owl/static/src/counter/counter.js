import { Component } from "@odoo/owl";


export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        id: {type: Number},
        val: {type: Number},
        callback:  {type: Function},
    }

    increment() {
        this.props.callback(this.props.id);
    }
}
