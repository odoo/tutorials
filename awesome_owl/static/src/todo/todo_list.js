/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.currentTodoInput = useState({ value: "" });
        this.todos = useState([
            { id: 0, description: "buy milk", isCompleted: false },
            { id: 1, description: "buy milk", isCompleted: true },
        ]);
        this._todoIdSequence = 2;

        useAutofocus("todoInputRef");
    }

    addTodo(e) {
        if (e.keyCode !== 13 || this.currentTodoInput.value.trim() === "") return;
        this.todos.push({
            id: this._todoIdSequence++,
            description: this.currentTodoInput.value.trim(),
            isCompleted: false,
        });
        this.currentTodoInput.value = "";
    }

    toggleState(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
