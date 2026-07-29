import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todoList";

export class Playground extends Component {
    static template = 'awesome_owl.playground';
    static components = { Counter, Card, TodoList };
    static props = {};

    value1 = "<div>content 1</div>"
    value2 = markup("<div>content 2</div>")

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
