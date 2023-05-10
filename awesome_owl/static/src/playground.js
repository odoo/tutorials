import { Component, useState } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value = this.state.value + 1;
    }
}
