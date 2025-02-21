/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    static props = {}

    setup() {
        this.todos = useState([{ id: 3, description: "buy milk", isCompleted: false }, { id: 4, description: "buy milk", isCompleted: false }]);
    }
}
