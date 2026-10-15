import {TodoItem} from "./TodoItem"
import {Component, useState} from "@odoo/owl";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem}

    setup() {
        this.todos = useState([
            {id: 1, description: "write code", isCompleted: true},
            {id: 2, description: "read code", isCompleted: false},
        ])
    }
}
