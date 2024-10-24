/** @odoo-module **/

import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";
import { Component, useState } from "@odoo/owl";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static props = {};

    setup() {
        this.addTodoItem = this.addTodoItem.bind(this);
        this.todos = useState([
            { id: 1, description: "todo 1", isCompleted: true },
            { id: 2, description: "todo 2", isCompleted: false },
            { id: 3, description: "todo 3", isCompleted: false },
        ]);

        this.todoIdCount = this.todos.length + 1;

        this.state = useState({ text: "" });

        this.inpuRef = useAutoFocus("input_description");

        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    }

    addTodoItem(ev) {
        if (ev.keyCode === 13) {
            this.todos.push({
                id: this.todoIdCount++,
                description: this.state.text,
                isCompleted: false,
            });
            this.state.text = "";
        }
    }

    toggleState(todoId) {
        this.todos[todoId - 1].isCompleted = !this.todos[todoId -1].isCompleted;
    }

    removeTodo(todoId) {
        let index = this.todos.findIndex(todo => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    static components = { TodoItem };
}
