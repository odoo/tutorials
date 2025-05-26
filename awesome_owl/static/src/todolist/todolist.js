/** @odoo-module **/

import { useState, Component } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        useAutofocus("input")
    }

    addTodo(ev){
        const value = ev.target.value.trim()
        if (value !== "" && ev.keyCode === 13) {
            this.todos.push({
                id: this.nextId++,
                description: value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }
}
