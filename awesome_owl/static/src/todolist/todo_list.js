/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = xml/* xml */`
        <div class="todo-item mb-2 p-2 border rounded">
            <h4>Todo List</h4>
            <div t-foreach="todos" t-as="todo" t-key="todo.id">
                <TodoItem todo="todo" />
            </div>
        </div>
    `;

    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 3, description: "buy milk", isCompleted: false },
            { id: 4, description: "complete assignment", isCompleted: false },
        ]);
    }
}