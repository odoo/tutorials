/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo-item";
import { useAutofocus } from "../util";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.idSequence = useState({ next: 0 });
        useAutofocus("todo-input-ref");
    }

    _createTodo(keyboardEvent) {
        if (keyboardEvent.keyCode !== 13 || keyboardEvent.target.value == "") return;

        this.todos.push({
            id: this.idSequence.next++,
            description: keyboardEvent.target.value,
            isCompleted: false
        })

        keyboardEvent.target.value = "";
    }

    _toggleTodo(id) {
        const todo = this.todos.find(todo => todo.id === id);
        if (todo) todo.isCompleted = !todo.isCompleted;
    }

    _removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index > -1) this.todos.splice(index, 1);
    }
}
