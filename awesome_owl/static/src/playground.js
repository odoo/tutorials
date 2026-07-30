import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, TodoList }

    content = markup("<div> some texte 2</div>")

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++
    }
}