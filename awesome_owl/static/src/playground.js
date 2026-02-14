import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
import { TodoList } from "./TodoList/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }

    setup() {
        this.state = useState({ v_sum: 2 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum(value) {
        this.state.v_sum = this.state.v_sum + value
    }
}
