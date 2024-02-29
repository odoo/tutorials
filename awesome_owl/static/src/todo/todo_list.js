/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    
    

    setup() {
        this.todos = useState([]);
        this.sequence = 1;
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
        useAutofocus("input");
    }

    toggleState(id) {
        for (let i = 0; i < this.todos.length; i++) {
            if(this.todos[i]["id"] == id) {
                this.todos[i]["isCompleted"] = !this.todos[i]["isCompleted"];
            }
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && !(document.querySelector('input').value.trim().length === 0)) {
            this.todos.push({
                id: this.sequence,
                description: document.querySelector('input').value,
                isCompleted: false,
                toggle: this.toggleState,
                remove: this.removeTodo
            });
            this.sequence++;
            document.querySelector('input').value = "";
        }
    }


    static components = { TodoItem };
}
