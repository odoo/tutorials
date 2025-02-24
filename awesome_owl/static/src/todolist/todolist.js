/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";


export class TodoList extends Component{
    static template = "awesome_owl.Todolist";
    setup(){
        this.todos = useState([
            {id: 3, description: "buy milk", isComplete: true},
            {id: 4, description: "buy honey", isComplete: false},
            {id: 5, description: "buy sugar", isComplete: false},
        ]);
    }
    static components = {TodoItem};
}
