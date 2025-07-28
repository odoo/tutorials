/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "learn Owl.js", isCompleted: true },
            { id: 3, description: "build todo app", isCompleted: false }
        ]);
        
        this.newTodoText = useState({ value: "" });
        this.nextId = 4; // Contatore semplice per i nuovi ID
    }

    addTodo() {
        const description = this.newTodoText.value.trim();
        if (description) {
            this.todos.push({
                id: this.nextId++,  // ID sempre crescente, mai riutilizzato
                description: description,
                isCompleted: false
            });
            this.newTodoText.value = "";
        }
    }

    onKeyPress(event) {
        if (event.key === 'Enter') {
            this.addTodo();
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
