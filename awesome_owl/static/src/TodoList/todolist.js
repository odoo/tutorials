import { Component } from "@odoo/owl"
import { TodoItem } from "../TodoItem/todoitem"

export class TodoList extends Component{
    static template = "awesome_owl.todolist"

    setup(){
        this.todos = [
            {id: 1, description: " go to office ", isComplete: true},
            {id: 2, description: " write code ", isComplete: false},
            {id: 3, description: " have a tea ", isComplete: false},
        ]
    }

    static components = { TodoItem }
}