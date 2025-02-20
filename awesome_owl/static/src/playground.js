import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter };
    setup() {
        this.state = useState({ count: 0 });
    }
    incrementsum() {
        this.state.count++;
    }
}
