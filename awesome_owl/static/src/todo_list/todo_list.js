/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {TodoItem} from "../todo_item/todo_item";
import {useAutofocus} from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.nextId = 0;
        this.todos = useState([]);
        useAutofocus("input")
    }

    addTodo(ev) {
        if (ev.key === 'Enter' && ev.target.value != "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
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
        if (todoIndex >= -1) {
            this.todos.splice(todoIndex, 1);
        }
    }
}