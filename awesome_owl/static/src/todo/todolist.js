/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = {TodoItem};

    setup(){
        this.todos = useState([{
            id: 0,
            description:"Milk",
            isCompleted:false
        }]);
        this.count = 1;
        this.inputRef = useAutofocus('input');
    }

    addTodo(ev){
        if (ev.keyCode === 13){
            const input = ev.target;
            const description = input.value.trim();
            if(!description){
                return;
            }
            const todo = {
                id : this.count,
                description : description,
                isCompleted : false
            };
            this.todos.push(todo);
            input.value = "";
            this.count++;
        }
    }

    toggleTodoState(todoId){
        const todo = this.todos.find(t => t.id === todoId)
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId){
        const todo_index = this.todos.findIndex(t => t.id === todoId)
        if(todo_index >= 0){
            this.todos.splice(todo_index, 1);
        }
    }
}
