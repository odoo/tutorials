import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./TodoItem";  
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextid = 0;
        useAutofocus("input")
    }

    toggleTodo(todoId){
        const todo = this.todos.find((todo) => todo.id == todoId);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push({
                id: this.nextid++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    removeTodo(todoId){
        const todoindex = this.todos.findIndex((todo) => todo.id == todoId);
        if(todoindex >= 0){
            
              this.todos.splice(todoindex , 1);
        }
    }
    
}
