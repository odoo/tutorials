/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import { TodoItem } from "../TodoItem/todoItem";
import {useAutofocus} from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup(){
        this.todos = useState([]);
        this.nextID = 1;
        useAutofocus("inputTask")
    }
    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value != ""){
            let newTodo = {id: this.nextID++, description: ev.target.value, isCompleted: false};
            this.todos.push(newTodo);
            ev.target.value = "";
        }
    }

    toggleTodo(value){
        console.log("toggleTodo function");
        console.log(value.isCompleted);
        
        value.isCompleted = !value.isCompleted;
    }

    deleteTodo(value){
        const index = this.todos.findIndex((elem) => elem.id === value.id);
        if(index >= 0){
            this.todos.splice(index, 1);
        }
        console.log(this.todos.length);
        console.log(this.todos);
    }
}
