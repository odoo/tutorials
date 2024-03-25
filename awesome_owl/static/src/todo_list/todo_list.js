/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.itemId = 1;
        this.todos = useState([]);
        useAutofocus("inputFoucs");
    }
    
    addTask(ev) {
        if (ev.keyCode == 13 && ev.target.value != "") {
            this.todos.push({
                id: this.itemId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleStatus(id) {
        if (this.todos) {
            this.todos.forEach(todo => {
                if (todo.id == id) {
                    todo.isCompleted = !todo.isCompleted;
                }
            });
        }
    }

    removeTask(id) {
        if (this.todos) {
            const index = this.todos.findIndex((task) => task.id === id);
            if (index >= 0) {
                this.todos.splice(index, 1);
            }
        }
    }
}
