/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        this.id = 1;
    }

    addTodo(event) {
        if (event.keyCode == 13) {
            let val = document.getElementById("idescription").value.trim();
            if (val.trim() != "") {
                this.todos.push({id: this.id++, description: val, isComplete: false})
                document.getElementById("idescription").value = ""
            }
        }
    }
}
