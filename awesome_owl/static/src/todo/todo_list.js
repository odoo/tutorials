/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    todos = useState([{ id: 3, description: "buy milk", isCompleted: false }])

    static template = xml`
        <div class="m-2">
            <t t-foreach="todos" t-as="todo" t-key="todo.id">
                <TodoItem id="todo.id" description="todo.description" isCompleted="todo.isCompleted"/>
            </t>
        </div>
    `

    static components = { TodoItem }
}