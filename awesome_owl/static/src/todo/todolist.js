/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { ToDoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class ToDoList extends Component {
    static template = "awesome_owl.ToDoList";
    static components = { ToDoItem };

    setup() {
        this.nextId = 0;
        this.todos = useState([]);
        useAutofocus("input");
    }

    addToDo(ev){
        if(ev.keyCode === 13 && ev.target.value != ""){
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleState(todoId){
        const todoCheck = this.todos.find((todo) => todo.id === todoId);
        if(todoCheck){
            todoCheck.isCompleted = !todoCheck.isCompleted;
        }
    }

    removeToDo(todoId){
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if(todoIndex >= 0){
            this.todos.splice(todoIndex,1);
        }
    }
}