/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        useAutofocus("inputRef");
        this.todos = useState([]);
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value !== "") {
            this.todos.push(
                {
                    id: 1 + Math.max(...this.todos.map(todo => todo.id), 0),
                    description: e.target.value,
                    isCompleted: false,
                },
            );
            e.target.value = "";
        }
    }

    removeTodo(id) {
        this.todos.splice(this.todos.findIndex(todo => todo.id === id), 1);
    }
}