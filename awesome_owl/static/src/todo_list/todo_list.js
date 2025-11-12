import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    setup(){
        this.todos = useState([]);
        this.nextId = 0;
        useAutofocus("input")
    }
    static components = {TodoItem}

    addToDo(ev){
        if(ev.keyCode === 13 && ev.target.value != "") {
            this.nextId++;
            this.todos.push({id:this.nextId, description: ev.target.value , isCompleted:false})
            ev.target.value = ""
        }
    }

    toggleToDo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        } 
    }

    deleteToDo(elemId) {
        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
        this.todos.splice(index, 1);
        }
    }  
}
