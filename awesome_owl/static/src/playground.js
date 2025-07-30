/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }
    html = ('<h3>hello world</h3>');
    markup_html = markup(this.html);

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
