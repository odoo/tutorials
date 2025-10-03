/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "@awesome_owl/utils";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        useAutofocus("input_task");
    }

    addTodo(event) {
        if (event.keyCode !== 13 || !event.target.value) {
            return;
        }
        let newId = 0;
        // TODO: This is not a good way to generate a new id
        // I would keep this list sorted by id
        // to not check all the list for each id
        while (this.todos.find((todo) => todo.id === newId)) {
            newId++;
        }
        this.todos.push({
            id: newId,
            description: event.target.value,
            isCompleted: false,
        });
        event.target.value = "";
    }

    toggleState(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        // find the index of the element to delete
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }
}
