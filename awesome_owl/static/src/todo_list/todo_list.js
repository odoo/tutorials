/** @odoo-module **/

import { filterInPlace, useAutofocus } from "../utils";
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 0, description: "commit murder", isCompleted: true },
            { id: 1, description: "uwu", isCompleted: false },
        ]);

        useAutofocus("todoInput");
    }

    addTodo(ev) {
        if (ev.keyCode !== 13) return;

        const description = ev.target.value.trim();

        // Since ids are in ascending order, the last id + 1 is always unique
        let id = 0;
        if (this.todos.length)
            id = this.todos.at(-1).id + 1;

        if (!description) return;

        this.todos.push({
            id,
            description,
            isCompleted: false,
        });
    }

    toggleTodo(id) {
        for (const todo of this.todos) {
            if (todo.id === id) {
                todo.isCompleted = !todo.isCompleted;
                break;
            }
        }
    }

    removeTodo(id) {
        this.todos = filterInPlace(this.todos, todo => id !== todo.id);
    }
}
