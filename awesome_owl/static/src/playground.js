/** @odoo-module **/

import { useState, markup, Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.html_title = markup("<div>Title </div>")
        this.state = useState({ sum: 0 })
        this.counter = new Counter;
    }

    incrementSum() {
        this.state.sum++;
    }
}
