/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Autofocus } from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            //{ id: 2, description: "eat fruit", isCompleted: true },
            //{ id: 3, description: "bees", isCompleted: false },
        
        ]);
        this.nextId = this.todos.length + 1;

        Autofocus("focus")
    }

    addTodo(ev) {
        // If enter key is pressed
        if (ev.keyCode === 13) {
            let newval = ev.target.value;
            if (newval.length !== 0) {
                this.todos.push({id: this.nextId, description: newval, isCompleted: false});
                this.nextId++;
            }
        }
    }
}
