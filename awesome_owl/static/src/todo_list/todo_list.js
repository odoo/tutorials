/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todo_list/todo_item";
import { useAutoFocus } from "@awesome_owl/utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {

        useAutoFocus("todo_input");

        this.todos = useState([]);
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value.trim() !== "") {
            let newIdx = 0
            if (this.todos.length !== 0) {
                newIdx = this.todos[this.todos.length - 1].id + 1
            }
            const newTodo = {
                id: newIdx,
                description: event.target.value.trim(),
                isCompleted: false
            };

            this.todos.push(newTodo);
            event.target.value = "";
        }
    }

    toggleState(todo_id) {
        const todo = this.todos.find((t) => t.id === todo_id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todo_id) {
        const targetIdx = this.todos.findIndex((t) => t.id === todo_id);
        if (targetIdx >= 0)
            this.todos.splice(targetIdx, 1);
    }

}
