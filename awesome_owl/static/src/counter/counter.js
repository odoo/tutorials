import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = 'counter.counter';
    setup() {
        this.counter = useState({value: 0});
    }

    increment() {
        this.counter.value++;
    }
}
