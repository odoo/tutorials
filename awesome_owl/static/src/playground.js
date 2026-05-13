import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./components/card/card";
import { Counter } from "./components/counter/counter";
import { TodoList } from "./components/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.card1Body = "<div>text without markup</div>";
        this.card2Body = markup("<div>text with markup</div>");
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
