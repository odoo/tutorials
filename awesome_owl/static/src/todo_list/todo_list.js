/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.nextId = 0;
        this.todos = useState([]);

        useAutofocus("todo_input")
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value !== "") {
            this.todos.push({
                id: this.nextId++,
                description: event.target.value,
                isCompleted: false
            });

            event.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}