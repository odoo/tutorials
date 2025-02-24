/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = {
        TodoItem,
    }

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
    }

    addTodo(event) {
        if (event.key == "Enter" && event.target.value!="") {
            this.todos.push({ id: this.nextId++, description: event.target.value, isCompleted: false });
            event.target.value = "";
        }
    }
    
}