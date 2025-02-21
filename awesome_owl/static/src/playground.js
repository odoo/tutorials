import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ value: 0, sum: 0 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    increment() {
        this.state.value++;
    }

    decrement() {
        this.state.value--;
    }

    incrementSum() {
        this.state.sum++;
    }
}
