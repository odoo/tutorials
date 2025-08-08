/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import TodoItem from "./todoitem";

export default class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props={};

    setup() {
        this.todos = useState([]);
        this.nextId = 1; 
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {  
            const description = ev.target.value.trim();
            if (description) {
                this.todos.push({
                    id: this.nextId++,
                    description,
                    isCompleted: false,
                });
                ev.target.value = "";
            }
        }
    }
    
    toggleState(id) {
        const todo = this.todos.find((t) => t.id === id);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((t) => t.id === id);
        if(index !== -1){
            this.todos.splice(index, 1)
        }
    }
}
