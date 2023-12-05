/** @odoo-module */

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { Todo } from "../todo/todo";

export class Todolist extends Component {
    static template = "owl_playground.Todolist";
    static components = { Todo };
    inputRef = useRef("input")

    setup(){
        this.currentId = 1;
        this.todolist = useState([]); 
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != ""){
            this.todolist.push({id: this.currentId++, description: ev.target.value, done: false});
            ev.target.value = "";
        }
    }
}
