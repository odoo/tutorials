/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutoFocuse } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };

    todos = useState([{ id: 3, description: "buy milk", isCompleted: true }]);
    uniqueId = 0;
    
    setup() {
        useAutoFocuse('todoInput');
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const value = ev.target.value.trim();
            if (value) {
                this.todos.push({id: this.uniqueId++, description: ev.target.value, isCompleted: false});
                ev.target.value = '';
            }
        }
    }

    toggleTodoState(todoId) {
        for(let todo of this.todos) {
            if (todo.id === todoId) {
                todo.isCompleted = !todo.isCompleted;
            }
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
