import { Component, useState, markup } from "@odoo/owl";

import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card"
import { TodoList } from "./components/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    sum = useState({ value: 0 })

    card1Content = "<div class='text-primary'>some content</div>"
    card2Content = markup("<div class='text-primary'>some content</div>")

    setup() {
        this.incrementSum = this.incrementSum.bind(this)
    }

    incrementSum() {
        this.sum.value += 1
    }
}
