/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = {
        TodoItem,
    }

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        useAutofocus("input");
    }

    addTodo(event) {
        if (event.key == "Enter" && event.target.value!="") {
            this.todos.push({ id: this.nextId++, description: event.target.value, isCompleted: false });
            event.target.value = "";
        }
    }
    toggleTodo(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }
}