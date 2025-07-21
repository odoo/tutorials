/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {    };
    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        useAutofocus("todoInput");
    }

    addTodo(event) {
        if (event.key === "Enter" && event.target.value!== "") {
            this.todos.push({
                id: this.nextId++,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find(todo => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}