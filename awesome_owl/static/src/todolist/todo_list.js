import {Component, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component{
    static components = {TodoItem};
    
    setup(){
        this.todos = useState([
            {id: 1, description: "Buy Milk", isCompleted: false},
            {id: 2, description: "Completd Owl tutorial", isCompleted: false},
            {id: 3, description: "Exercise completed", isCompleted: false},
        ]);
        console.log(this.todos);
    }
}

TodoList.template = "awesome_owl.todo_list";