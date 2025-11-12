/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";


export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.inputTodoRef = useRef('inputTodo');
        this.currentdescription = useState(
            {
                value: ''
            }
        );
    };

    addTodo() {
        if(this.currentdescription.value.trim() != ''){
            this.todos.push({
                id: this.todos.length + 1,
                description: this.currentdescription.value,
                isCompleted: false
            });
        }
        this.currentdescription.value = ''
        this.inputTodoRef.el.focus();
    }

    toggleState(id){
        this.todos[id-1].isCompleted = !this.todos[id-1].isCompleted;
    }

    removeTodo(id){
        this.todos.splice(id-1,1);
        for(let i = id-1; i<this.todos.length; i++){
            this.todos[i].id = i+1
        }
    }
}
