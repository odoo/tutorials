import { Component, useState } from "@odoo/owl";
import {ToDoItem}  from "./todoitem";

export class ToDoList extends Component {
    static template = "awesome_owl.ToDoList";
    static components = { ToDoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: true },
            { id: 2, description: "buy chocolate", isCompleted: true },
            { id: 3, description: "sell both", isCompleted: false },
        ])
    }
}