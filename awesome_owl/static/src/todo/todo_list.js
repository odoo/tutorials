import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils/utils";

export class TodoList extends Component{
    static template = "awesome_owl.todo_list"
    static components = {TodoItem}

    setup(){
        this.todos = useState([
            {id:1,description:"milk",isCompleted:true}
        ]);
        this.nextId =2;
        this.inputRef = useRef("todoInput")
        useAutofocus(this.inputRef)
    }
    addTodo(ev){
        if(ev.keyCode === 13){
            const description = this.inputRef.el.value.trim();
            if(description){
                this.todos.push({
                    id: this.nextId++,
                    description,
                    isCompleted: false,
                });
                this.inputRef.el.value="";
                this.inputRef.el.focus()
            }
        }
    }
    togglestate(id){
        const todo = this.todos.find(t=> t.id === id)
        if(todo){
            todo.isCompleted = !todo.isCompleted
        }
    }
    removeTodo(id){
        const index = this.todos.findIndex(t => t.id === id)
        if(index !== -1){
            this.todos.splice(index,1)
        }
    }
}