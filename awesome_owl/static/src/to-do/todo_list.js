/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.newId = 0;
        this.inputRef = useRef("input");
        useAutoFocus(this.inputRef);
    }

    addTodo = (event) => {
        if (event.keyCode === 13 && event.target.value != "") {
            this.newId++;
            this.todos.push({
                id: this.newId,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    };

    toggleTodo = (todoId) => {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    };

    deleteTodo = (todoId) => {
        const index = this.todos.findIndex((elem) => elem.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    };
}