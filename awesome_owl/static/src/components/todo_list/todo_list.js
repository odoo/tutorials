/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [],
            nextId: 1,
            newTodo: "",
        });
    }

    addTodo = (ev) => {
        ev.preventDefault();
        const description = this.state.newTodo.trim();
        if (description) {
            this.state.todos.push({
                id: this.state.nextId++,
                description,
                isCompleted: false,
            });
            this.state.newTodo = "";
        }
    }

    toggleTodo = (id) => {
        const todo = this.state.todos.find((t) => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo = (id) => {
        this.state.todos = this.state.todos.filter((t) => t.id !== id);
    }
}
