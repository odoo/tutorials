/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { Todo } from "../todo/todo";

export class Todolist extends Component {
    static template = "owl_playground.Todolist";
    static components = { Todo };

    setup(){
        this.currentId = 1;
        this.todolist = useState([]); 
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != ""){
            this.todolist.push({id: this.currentId++, description: ev.target.value, done: false});
            ev.target.value = "";
        }
    }
}
