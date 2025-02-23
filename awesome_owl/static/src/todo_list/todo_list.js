/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.myRefInput = useAutofocus("todoInput");
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();
            if (description) {
                this.todos.push({ id: this.nextId++, description, isCompleted: false });
                input.value = "";
                input.focus();
            }
        }
    }

    toggleStateChange(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodoFromList(todoId) {
        const index = this.todos.findIndex(todo => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
