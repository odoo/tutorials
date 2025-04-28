/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static props = { };

    setup() {
        this.todos = useState([]);
    }

    addTodo(e) {
        if (e.keyCode !== 13) return;
        let value = e.target.value;
        if (value === "") return;
        this.todos.push({
            id: this.todos.length,
            description: value,
            isCompleted: false
        });
        e.target.value = "";
    }
}
