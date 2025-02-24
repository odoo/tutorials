/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    static props = {}

    setup() {
        this.todos = useState([]);
        this.count = 1;
    }

    addItem(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.todos.push({id: this.count++, description: ev.target.value, isCompleted: false});
            ev.target.value = "";
        }
    }
}
