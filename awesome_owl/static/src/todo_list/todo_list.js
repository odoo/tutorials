/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup(){
        this.todos = useState([]);
        this.id = 0;
        useAutoFocus("input_todo");
    }

    toggleTodo(id){
        const todo = this.todos.find((todo) => todo.id === id);
        if(todo)
            todo.isCompleted = !todo.isCompleted;
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value !== ""){
            this.todos.push({
                id: this.id ++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }
}
