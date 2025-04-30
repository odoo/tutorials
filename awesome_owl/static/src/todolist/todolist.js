/** @odoo-module **/

import { useState, Component } from "@odoo/owl";

import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    
    todos = useState([
        { id: 2, description: "write tutorial", isCompleted: false }, 
        { id: 3, description: "buy milk", isCompleted: false }
    ]);
}
