import { Component, markup, useState } from "@odoo/owl";
import { Counter } from './counter/counter';
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};

    html = markup('<a href="https://www.google.com" target="_blank" rel="noopener noreferrer">Some content</a>');

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
