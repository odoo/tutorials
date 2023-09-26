/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

import { Todo } from './todo/todo'
import { useAutofocus } from "../utils";

export class TodoList extends Component {


    setup() {
        useAutofocus('todosInput')
        this.todos = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push({
                id: this.todos.length + 1,
                description: ev.target.value,
                done: false
            });
            ev.target.value = "";
        }
    }

    toggleDone(todoId) {
        const todoItemidx = this.todos.findIndex(item => item.id === todoId)
        if (todoItemidx >= 0) {
            this.todos[todoItemidx].done = !this.todos[todoItemidx].done;
        }
    }

    removeTodo(todoId) {
        const todoItemidx = this.todos.findIndex(item => item.id === todoId)
        if (todoItemidx >= 0) {
            this.todos.splice(todoItemidx, 1)
        }
    }
}

TodoList.template = "owl_playground.todo_list"
TodoList.components = { Todo }
