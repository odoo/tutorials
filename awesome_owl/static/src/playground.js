import { Component, useState } from "@odoo/owl";
import { Counter } from './Counter'
import { Card } from "./Card"
import { TodoList } from "./TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList }

    setup() {
        this.state = useState({ sum: 0 })
        this.incrementSum = this.incrementSum.bind(this)
    }

    incrementSum() {
        this.state.sum++;
    }
}
