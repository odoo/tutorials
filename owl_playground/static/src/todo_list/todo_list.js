/** @odoo-module */

import { Todo } from "../todo/todo";

import { Component } from "@odoo/owl";

export class TodoList extends Component {
    static template = "owl_playground.TodoList";
    setup() {
        this.todoList = [
            { id: 3, description: "buy milk", done: false },
            { id: 4, description: "buy eggs", done: true },
            { id: 5, description: "buy avocado", done: true },
        ];
    }

    static components = { Todo };
}

