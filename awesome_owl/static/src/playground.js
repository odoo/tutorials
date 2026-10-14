import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }

    setup() {
        this.withMarkup = markup("<div class='text-success fw-bold'> With Markup HTML </div>");
        this.withoutMarkup = "<div class='text-danger fw-bold'> Without Markup </div>";
        this.state = useState({sum: 2});
    }

    incrementSum() {
        this.state.sum++;
    }
}
