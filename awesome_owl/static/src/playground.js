import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    setup() {
        this.escapedHtml = "This is <b>escaped</b> text (rendered as plain text)";
        this.safeHtml = markup("This is <b>markup HTML</b> text (rendered as actual HTML)");
        this.state = useState({ sum: 0 });
    }

    updateSum(val) {
        this.state.sum += val;
    }
}
