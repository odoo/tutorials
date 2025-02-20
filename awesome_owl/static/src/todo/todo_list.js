/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_items";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.newTask = useState({ description: "" });
        useAutofocus("todoInput");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.todos.push({
                id: Date.now(),
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        this.todos.splice(this.todos.findIndex((t) => t.id === todoId), 1);
    }
}
