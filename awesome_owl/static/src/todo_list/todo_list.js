/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { TodoItem } from "./todo_item/todo_item";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = {
        TodoItem,
    };

    setup() {
        this.todos = useState([]);
        this.nextIndex = 0;
        useAutofocus("input_ref");
    }

    addTodo(ev) {
        let input_val = ev.target.value;
        if (ev.keyCode === 13 && input_val != "") {
            this.todos.push({
                id: this.nextIndex++,
                description: input_val,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    removeTodoFromList(todoId) {
        let index = this.todos.findIndex(todo => todo.id === todoId);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
