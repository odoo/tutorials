/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    
    todos = useState([]);
    inputRef = useAutoFocus()

    addTodo(e) {
        let todoTitle = e.target.value;

        if (e.keyCode === 13 && todoTitle) {
            this.todos.push({ id: this.todos.length ? this.todos[this.todos.length - 1].id + 1 : 0, description: todoTitle, isCompleted: false });
            e.target.value = "";
        }
    }

    toggleState(id) {
        let todo = this.todos.find((todo) => todo.id === id)
        if (todo) todo.isCompleted = !todo.isCompleted
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id)
        this.todos.splice(index, 1)
    }
}
