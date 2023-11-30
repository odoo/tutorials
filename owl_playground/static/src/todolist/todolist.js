/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Todo } from './todo/todo'
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "owl_playground.todolist";
    static components = { Todo };

    setup() {
        this.inputElement = useAutofocus("todoInput");
        this.state = useState({
            id: 5,
            todos: [
                { id: 1, description: "buy milk 1", done: false },
                { id: 2, description: "buy milk 2", done: true },
                { id: 3, description: "buy milk 3", done: false },
                { id: 4, description: "buy milk 4", done: true }
            ],
            description: ''
        });
    }

    addTodo(event) {
        if (event.keyCode === 13 && this.state.description !== '') {
            this.state.todos.push({ id: this.state.id++, description: this.state.description, done: false });
            this.state.description = '';
        }
    }

    toggleState(id) {
        this.state.todos = this.state.todos.map(todo => todo.id === id ? { ...todo, done: !todo.done } : todo);
    }

    removeTodo(id) {
        this.state.todos = this.state.todos.filter(todo => todo.id !== id);
    }
}
