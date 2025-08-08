/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";

import { Counter } from "./components/counter/counter";

import { Card } from "./components/card/card";
import { TodoList } from "./components/todo/todo";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList }

    setup() {
        this.state = useState({sum: 0});
        this.card_content = markup("<div style='color: blue'>some content in here</div>");
        this.increment = this.increment.bind(this);

        this.card1_title_slot = markup("<h3>Counter 1</h3>")
        this.card2_title_slot = markup("<h3>Counter 2</h3>")
    }

    increment() {
        this.state.sum++;
    }
}
