/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.newId = 1;
    }
    addTodo(e) {
        if (e.keyCode === 13 && e.target.value != "") {
            this.todos.push({
                id: this.newId++,
                description: e.target.value,
                isCompleted: false
            })
            e.target.value = ""
        }
    }
}
