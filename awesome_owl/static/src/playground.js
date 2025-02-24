/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";
import { TodoItem } from "./todolist/todoitem";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({ sum: 0 })
    }

    incrementSum() {
        this.state.sum += 1;
    }

    static components = { Counter, Card, TodoList, TodoItem };
}
