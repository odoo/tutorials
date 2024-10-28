/** @odoo-module **/
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList, TodoItem } from "./todo/todo";
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoItem, TodoList };
    html = markup("<div class='text-primary'>some content</div>");

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
