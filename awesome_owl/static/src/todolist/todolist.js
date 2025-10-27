/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "take a coffe", isCompleted: true },
            { id: 2, description: "write tutorial", isCompleted: false },
            { id: 3, description: "buy milk", isCompleted: false }
        ]);

        useAutofocus("addTodo-input");
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value !== "") {
            this.todos.push({ id: this.todos.length + 1, description: ev.target.value.replace(/\n/g, ''), isCompleted: false });
            ev.target.value = "";
        }
    }

    removeTodo(idToRemove) {
        const index = this.todos.findIndex((elem) => elem.id === idToRemove);
        if (index >= 0) {
            this.todos.splice(index, 1);
            for(let i=index; i<this.todos.length; i++){
                this.todos[i].id--;
            }
        }
    }

}
