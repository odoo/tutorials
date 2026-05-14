import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from './todo/todolist'


export class Playground extends Component {
    static template = "awesome_owl.playground";
    setup() {
        this.title = "<div>Hello dosto</div>"
        this.content = markup("<div>Hello dosto</div>")
        this.sum = useState({ value: 2 })
    }
    calcSum(str) {
        if (str == 'Increment') this.sum.value++
        else this.sum.value--

    }
    static components = { Counter, Card, TodoList }
}
