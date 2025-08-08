/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component{
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.nextId = 0;
        useAutofocus("todoValueInput");
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value != ""){
            this.todos.push({
                id : this.nextId++,
                description : ev.target.value,
                isCompleted : false
            })
            ev.target.value = "";
        }
    }

    toggleTodo(todoId){
        const todo = this.todos.find((todo) => todo.id === todoId);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId){
        const index = this.todos.findIndex((el) => el.id === todoId);
        if(index>=0){
            this.todos.splice(index,1);
        }
    }
}
