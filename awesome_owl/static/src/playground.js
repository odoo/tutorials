import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    setup() {
        this.safeHtml = markup("<b>Rendered HTML</b>");
        this.normalText = "<b>This will be escaped</b>";
        this.state = useState({
            sum: 2,
        });
    }
    incrementSum() {
        this.state.sum++;
    }
}

Playground.props = {};
