/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.id = 1;
        this.todos = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.todos.push({
                id: this.id++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }
}