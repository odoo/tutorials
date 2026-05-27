import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList};

    setup() {
        this.state = useState({ value: 2, sum: 0 });
        this.cardContent = markup("This content is <b>bold</b>");
    }

    increment() {
        this.state.value++;
    }

    incrementSum() {
        this.state.sum++;
    }
}
