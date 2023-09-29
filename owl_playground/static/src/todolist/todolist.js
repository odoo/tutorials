/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Todo } from "../todo/todo";
import { useAutofocus } from "../utils";


export class Todolist extends Component {
    static components = { Todo };
    static template = "owl_playground.todolist";

    setup() {
        this.todoList = [];
        this.todoList = useState([{ id: 1, description: "Task 1", done: false },{ id: 2, description: "Task 2", done: false },{ id: 3, description: "Task 3", done: false }]);
        this.nextId = this.todoList.length+1;
        this.inputred = useAutofocus("inputElement");
    }

    addTodo(ev) {
        if(ev.keyCode === 13){
            if (ev.target.value.trim() != "") {
                this.todoList.push({ id: this.nextId++, description: ev.target.value, done: false });
            }
            ev.target.value = "";
        }
    }

    toggleState(todoId) {

        const todo = this.todoList.find((todo) => todo.id === todoId);
        if (todo) {
            todo.done = !todo.done;
        }
    }
    removeTodo(todoId) {
        const index = this.todoList.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todoList.splice(index, 1);
        }
    }

    resetList(){
        this.todoList.splice(0);
    }
}
