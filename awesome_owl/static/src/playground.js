import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter };

    setup() {
        this.state = useState({ sum: 0 });
        this.counterValues = [0, 0];

        this.onCounter0Change = (value) => this.incrementSum(0, value);
        this.onCounter1Change = (value) => this.incrementSum(1, value);
    }

    incrementSum(index, value) {
        this.counterValues[index] = value;
        this.state.sum = this.counterValues.reduce((c1,c2) => c1+c2, 0);
    }
}