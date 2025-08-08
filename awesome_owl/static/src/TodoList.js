import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./TodoItem";  

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";  
    static components = { TodoItem };  

    setup() {
        
        this.todos = useState([
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Buy  tea from store", isCompleted: false },
        ]);
    }
}
