import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {
        TodoItem,
    }

    todos = [
        { id: 1, description: "buy sugar", isCompleted: false }, 
        { id: 2, description: "buy cereal", isCompleted: false },
        { id: 3, description: "buy milk", isCompleted: false }
    ];
}
