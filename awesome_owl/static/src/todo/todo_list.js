/** @odoo-module **/

import { Component, useState, xml, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = xml`
        <h2>TODO List</h2>
        <input placehold="Enter a new task" t-on-keyup="addTodo" t-ref="todo_input" />
        <table>
            <thead><tr>
                <t t-foreach="todoKeys" t-as="key" t-key="key">
                    <th><t t-out="key" /></th>
                </t>
            </tr></thead>
            <tbody>
                <t t-foreach="todos" t-as="todo" t-key="todo.id">
                    <TodoItem todo="todo" toggleState.bind="toggleTodoState" remove.bind="removeTodo" />
                </t>
            </tbody>
        </table>
    `;
    static components = { TodoItem };
    todoKeys = ['', 'ID', 'Description'];
    todos = useState([
        // {id: 0, description: "eat breakfast", isCompleted: true},
        // {id: 1, description: "take a walk", isCompleted: false},
        // {id: 2, description: "buy milk", isCompleted: false},
        // {id: 3, description: "go to work", isCompleted: true},
    ]);

    setup() {
        useAutofocus('todo_input');
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value) {
            this.todos.push({id: this.todos.length, description: event.target.value, isCompleted: false});
            event.target.value = "";
        }
    }

    toggleTodoState(id) {
        this.todos[id].isCompleted = !this.todos[id].isCompleted;
    }

    removeTodo(id) {
        this.todos.splice(id, 1);
        for (let id = 0; id < this.todos.length; id++) {
            this.todos[id].id = id;
        }
    }
}
