import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./TodoItem";
import { useAutofocus } from "../utils";

export class TodoList extends Component{
    static template = "awesome_owl.TodoList"

    static components = { TodoItem }

    setup(){
        this.todoItems = useState([]);
        this.nextId = 0;
        useAutofocus("todoInput");
    }

    addTodo(event){
        if(event.keyCode === 13){
            const description = event.target.value.trim();
            if(description.length){
                this.todoItems.push({id: this.nextId++, description: description, isCompleted: false})
                event.target.value = ""
            }
        }
    }

    toggleState(todoId){
        const todo = this.todoItems.find(item => item.id === todoId);

        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(todoId) {
        const index = this.todoItems.findIndex(todo => todo.id === todoId);
        
        if (index >= 0) {
            this.todoItems.splice(index, 1); 
        }
    }
};