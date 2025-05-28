import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.todos = useState([
                {id: 1, description: "Buy groceries", isCompleted: false},
                {id: 2, description: "Walk the dog", isCompleted: false},
                {id: 3, description: "Read a book", isCompleted: true},
            ],
        );
    }
}