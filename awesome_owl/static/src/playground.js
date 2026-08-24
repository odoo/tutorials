import { Component, useState } from "@odoo/owl";

import { Counter } from "./components/counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter };

    counter = useState({ value: 0 });

    increment() {
        this.counter.value += 1
    }
}
