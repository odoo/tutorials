import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            safeString: "<h1>This will be escaped</h1>",
            htmlContent: markup("<h1>This is bold content</h1>"),
            value: 0,
        });
        this.sum = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }

    incrementSum() {
        this.sum.value++;
    }
}
