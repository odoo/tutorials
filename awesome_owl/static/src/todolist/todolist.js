/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }

    setup() {
        this.todos = useState([
            { id: 0, description: "Buy house", isCompleted: true },
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Buy chocolate", isCompleted: true },
            { id: 3, description: "Clean house", isCompleted: false },
            { id: 4, description: "Pay bills", isCompleted: false },
            { id: 5, description: "Call mom", isCompleted: true },
            { id: 6, description: "Go on holiday", isCompleted: false },
        ]);
        this.id_counter = this.todos.length;
        useAutofocus("todolist_input");
    };

    addTodo(ev) {
        if (ev.keyCode === 13) {
            let desc = ev.target.value;
            if (desc) {
                this.todos.push({
                    id: this.id_counter++,
                    description: desc,
                    isCompleted: false
                });
                ev.target.value = "";
            }
        }
    };

    toggleState(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        this.todos[index].isCompleted = !this.todos[index].isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
