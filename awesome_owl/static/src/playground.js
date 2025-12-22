import { markup, useState, Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo-list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }

    someHtmlEscaped = "<div class='text-primary'>My content</div>";
    someHtml = markup("<div class='text-primary'>My content</div>");
}
