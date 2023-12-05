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

    toggleState(this_id){
        const this_todo = this.todolist.find((todo) => todo.id === this_id);
        if (this_todo) {
            this_todo.done = !this_todo.done;
        }
    }

    removeTodo(this_id){
        const this_index = this.todolist.findIndex((todo) => todo.id === this_id);
        if (this_index >= 0){
            this.todolist.splice(this_index, 1)
        }
    }
}
