import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static props = {
        callback: {type: Function, optional: true}
    }

    static template = "awesome_owl.counter.counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if(this.props.callback){
            this.props.callback(1)
        }
    }
}
