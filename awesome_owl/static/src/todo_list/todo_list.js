/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    
    static components = { TodoItem }

    setup() {
        this.todos = useState([
            {
                id: 2,
                description: "videos",
                isCompleted: true,
            },
            {
                id: 3,
                description: "buy milk",
                isCompleted: false,
            },
        ]);
        useAutofocus('todo_input');
    }

    addTodo(ev) {
        if (ev.key == "Enter") {
            let description = ev.target.value.trim();
            if (description.length > 0) {
                this.todos.push({
                    id: Math.max(...this.todos.map((t) => t.id)) + 1,
                    description: description,
                    isCompleted: false,
                });
            }
        }
    }

    toggleTodo(id) {
        let todo = this.todos.find((t) => t.id == id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        let index = this.todos.findIndex((t) => t.id == id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
