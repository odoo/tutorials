/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../TodoItem/todoItem";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    setup(){
        this.todos = useState([
            { id: 1, description: "Buy a pen", isCompleted: false },
            { id: 2, description: "Write Tutorial", isCompleted: true },
            { id: 3, description: "Buy milk", isCompleted: false }
        ]);
    }
    static components = {TodoItem};
}
