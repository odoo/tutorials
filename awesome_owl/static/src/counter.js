import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 0 , sum: 0});
        this.newstate = useState({ newval: 1 });
    }

    increment() {
        this.state.value++;
        console.log(this.state.value);
    }

    multiple() {
        this.newstate.newval = this.newstate.newval*2;
        console.log(this.newstate.newval);
    }

    sum() {
        this.state.sum = this.state.value + this.newstate.newval
    }
}
