/** @odoo-module **/

import { Component, markup, useState} from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
import { TodoList } from "./Todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};

    setup() {
        this.state = useState({ sum: 0 });
        this.incrementSum = () => {
            this.state.sum++;
        };
    }
}
