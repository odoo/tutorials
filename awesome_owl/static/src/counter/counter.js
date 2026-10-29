import { Component, signal } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter"; 
    
    setup() {
        this.state = signal({ value: 0 });
    }

    increment() {
        this.state.value++;
    }

}