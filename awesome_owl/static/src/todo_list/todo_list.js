/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.nextId = 0;
        this.newtodo = useState([]);
        useAutofocus("input")
    }
    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.newtodo.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }
    toggleTodo(todoId) {
        const todo = this.newtodo.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId) {
        const todoIndex = this.newtodo.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0) {
            this.newtodo.splice(todoIndex, 1);
        }
    }
}
