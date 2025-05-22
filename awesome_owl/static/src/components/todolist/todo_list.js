import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem};

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("input")
        // this.toggleTodo = this.toggleTodo.bind(this);
    }

    addTodo(item){
        if(item.key === 'Enter'){
            const input = item.target;
            const description = input.value.trim();

            if(!description){
                return;
            }
            else{
                this.todos.push({
                    id: this.nextId++,
                    description,
                    isCompleted : false
                });
                input.value = ""
            }
        }
    }

    toggleTodo=(id)=>{
        const todo = this.todos.find(prev => prev.id === id);
        if(todo){
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodoItem=(todoId)=> {
        const index = this.todos.findIndex(todo => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

}