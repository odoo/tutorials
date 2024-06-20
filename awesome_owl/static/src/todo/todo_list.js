/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item.js"

export class TodoList extends Component {

    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.taskCounter = 0;
    }

    addTodo(ev) {
        if (ev.keyCode != 13 || ev.srcElement.value === "")
            return;

        this.todos.push({ id: this.taskCounter, description: ev.srcElement.value, isCompleted: false });
        ev.srcElement.value = "";
        this.taskCounter++;
    }
}