import { Component, signal } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    count = signal(0);

    increment() {
    this.count.set(this.count() + 1);
    }

    reset() {
    this.count.set(0);
    }
}