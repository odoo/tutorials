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

    title1 = "Card 1";
    title2 = "Card 2";
    content1 = "<div class='text-primary'>My content</div>";
    content2 = markup("<div class='text-primary'>My content</div>");
}
