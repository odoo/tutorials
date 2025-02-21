import {Component, useState} from "@odoo/owl"
import { TodoItem } from "./todo_item"

export class TodoList extends Component{
    static template = "awesome_owl.todoList"
    static components = {TodoItem}
    setup(){
        this.nextId = 1
        this.todos = useState([]);
    }

    addTodo(event){
        if(event.keyCode === 13 && event.target.value != ""){
            this.todos.push({
                id: this.nextId++,
                description: event.target.value,
                isCompleted: false
            })
            event.target.value = ""
        }
    }
}
