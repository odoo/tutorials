import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup(){
        this.state = useState({
            todos: [
                { id:1, description: "Read documentation", isCompleted: true},
                { id:2, description: "Complete Collage Work", isCompleted: false},
                { id:3, description: "Bought Milk", isCompleted: true},
                { id:4, description: "something", isCompleted: true},
                { id:5, description: "somethingpending Task", isCompleted: true},
                { id:6, description: "Try to complete task", isCompleted: true}
            ]
        });
    }
}
