/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card"
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.cards = [
            { title: "Card 1", content: "This is a normal text." },
            { title: "Card 2", content: markup("<b>This is bold text</b>") },
            { title: "Card 3", content: markup("<i>This is italic text</i>") }
        ];
        this.state = useState({ sum: 0 });
        // this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum(newValue) {
        this.state.sum += newValue;
    }
}
