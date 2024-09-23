/** @odoo-module */

import {Component, useState} from '@odoo/owl'
import {TodoItem} from "@awesome_owl/todo/todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.todo.todo_list"
    static components = {TodoItem}

    setup() {
        this.currentId = 0;
        this.state = useState({
            todos: [],
            newTodo: "",
        })
    }

    sanitizeTodo() {
        this.state.newTodo = this.state.newTodo.trim();
        return this.state.newTodo;
    }

    removeTodoItem(id) {
        this.state.todos = this.state.todos.filter((todo) => todo.id !== id);
    }

    addTodo() {
        if (!this.sanitizeTodo()) {
            return;
        }
        this.state.todos.push({
            id: this.currentId++,
            name: this.state.newTodo,
            done: false,
            dateAdded: new Date().getTime(),
            dateCompleted: null,
        });
        this.state.newTodo = "";
    }

    addTodoOnEnter(ev) {
        if (ev.key === "Enter") {
            this.addTodo();
        }
    }
}