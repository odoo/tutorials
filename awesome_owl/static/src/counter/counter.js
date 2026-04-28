import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    static props = {
        onincrement : { type: Function, optional: true },
        ondecrement : { type: Function, optional: true }
    };

    setup() {
        this.count = useState({value:0});
    }

    increment() {
        this.count.value++;
        if(this.props.onincrement){
            this.props.onincrement();
        }
    }

    decrement() {
        this.count.value--;
        if(this.props.ondecrement){
            this.props.ondecrement();
        }
    }

}
