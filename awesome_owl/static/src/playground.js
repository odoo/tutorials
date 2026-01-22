/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter.js"
import { Card } from "./card/card.js"
import { TodoList } from "./todo/todoList.js";
export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList }

    setup() {
        this.state = useState({ counterSum: 2 })
        this.markupContent = { cardContent: markup("<a href='#'>some_content</a>") }
    }

    onCounterIncrement() {
        this.state.counterSum++;
    };
}
