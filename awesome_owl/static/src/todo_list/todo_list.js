/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { useAutoFocus } from "../utils";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        useAutoFocus('input')
        this.todos = useState([]);
        this.newId = 1;
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value != "") {
            this.todos.push({
                id: this.newId++,
                description: e.target.value,
                isCompleted: false
            })
            e.target.value = ""
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
    
}
