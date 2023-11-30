/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Todo } from "./todo/todo";

export class Playground extends Component {
    static template = "owl_playground.playground";

    static components = { Counter, Todo };

    todos = [
        { id: 1, description: "buy milk 1", done: false },
        { id: 2, description: "buy milk 2", done: true },
        { id: 3, description: "buy milk 3", done: false },
        { id: 4, description: "buy milk 4", done: true },
    ]
}
