import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from '../utils';

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static props = {
        todos: { type: Array, optional: true }
    };
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Walk the dog", isCompleted: false },
            { id: 3, description: "Do laundry", isCompleted: false }
        ]);
        useAutofocus("myInput");
    }

    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value) {
            this.todos.push({ id: this.todos.length + 1, description: ev.target.value, isCompleted: false });
            ev.target.value = "";
            return;
        } else {
            return;
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
