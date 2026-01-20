/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";
import { Card } from "../card/card";
import { TodoList } from "../todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            sum: 2
        });

        this.title1 = "Card 1";
        this.title2 = "Card 2";
    }

    incrementSum() {
        this.state.sum++;
    }
}
