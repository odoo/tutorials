/** @odoo-module */

import { Component } from "@odoo/owl";
import { Todo } from "../todo/todo";

export class Todolist extends Component {
    static template = "owl_playground.Todolist";
    static components = { Todo };

    setup(){
        this.todolist = [
            { id: 3, description: "buy milk", done: false },
            { id: 4, description: "buy eggs", done: true },
            { id: 5, description: "buy avocado", done: true },
        ];
    }
}
