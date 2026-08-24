import { Component, useState } from "@odoo/owl";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    counter = useState({ value: 0 });

    increment() {
        this.counter.value += 1
    }
}
