/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    index = 0;

    setup() {
        this.todos = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != '') {
            this.todos.push({ id: ++this.index, description: ev.target.value, completed: false, });
            ev.target.value = '';
        }
    }
}
