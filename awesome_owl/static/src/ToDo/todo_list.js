/** @odoo-module **/

import { Component, useState, setState } from "@odoo/owl";
import { TodoItem } from "./todo_item"
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.todos = useState(new Array());
        useAutofocus("input");
    }

    onInputEnter(event) {
        if (event.keyCode === 13 && event.target.value != "") {
            this.todos.push({ "id": this.todos.length + 1, "description": event.target.value, "isCompleted": false });
            event.target.value = "";
        }
    }

    toggle(id) {
        for (let todo of this.todos) {
            if (todo.id === id) {
                todo.isCompleted = !todo.isCompleted;
            }
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
