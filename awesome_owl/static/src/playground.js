import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 0 });
    }

    card1Content = markup("<div>Some Text in div Tag</div>");
    card2Content = "<div>Some Text in div Tag</div>";

    incrementSum() {
        this.state.sum++;
    }
}
