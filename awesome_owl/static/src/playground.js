import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };

    setup() {
        this.htmlContent = markup("<em class='text-success'>some content!</em>");
        this.state = useState({ sum: 2 });
    }

    incrementSum = () => {
        this.state.sum++;
    }
}
