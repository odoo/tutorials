/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    setup() {
        this.state = useState({ value: 0, sum: 0 })
        this.calculateSum = this.calculateSum.bind(this);
    }

    increment() {
        this.state.value++
        this.calculateSum(this.state.value)
    }

    decrement() {
        return this.state.value <= 0 ? 0 : this.state.value--
    }

    calculateSum(value) {
        this.state.sum = this.state.value + value
    }
}
