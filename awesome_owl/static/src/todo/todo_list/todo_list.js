/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutoFocus } from "../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.count = useState({ value: 0 });
        useAutoFocus("todo_input");
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value) {
            this.count.value ++;
            this.todos.push({
                id: this.count.value,
                description: event.target.value,
                isCompleted: false
            });
            event.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(todo => todo.id === id)
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo (id) {
        const index = this.todos.findIndex((todo) => todo.id === id)
        if (index >= 0) {
            this.todos.splice(index, 1);
      }
    }
}
