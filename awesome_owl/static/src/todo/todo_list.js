/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        this.id = 1;

        useAutofocus("description");
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

    toggleState(todoId) {
        let todo = this.todos.find(todo => todo.id === todoId);
        if (todo) {
            console.log(todo)
            todo.isComplete = !todo.isComplete;
        }
    }

    onRemove(todoId) {
        const index = this.todos.findIndex(todo => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
