/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }
    ENTER_KEY_CODE = 13;

    setup() {
        this.state = useState({ todos: [{ id: 1, description: "buy milk", isCompleted: false }] })
        this.inputRef = useRef('input_todo');
    }

    addTodo(event) {
        if (event.keyCode === this.ENTER_KEY_CODE && event.target.value) {
            this.state.todos.push({
                id: this.state.todos.length ? Math.max(...this.state.todos.map(e => e.id)) + 1 : 1,
                description: event.target.value,
                isCompleted: false
            })
            this.inputRef.el.value = '';
        }
    }

    toggleTodo(todo) {
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(todo) {
        this.state.todos = this.state.todos.filter(t => t.id !== todo.id)
    }
}
