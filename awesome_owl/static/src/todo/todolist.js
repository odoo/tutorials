/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
// Custom elements
import { TodoItem } from "./todoitem";
import { autoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    nextID;

    setup() {
        this.nextID = 1;

        this.todos = useState([]);
        autoFocus("user_input");
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value != '') {
            this.todos.push({
                id: this.nextID,
                description: event.target.value,
                isCompleted: false
            });
            this.nextID++;
            event.target.value = "";
        }
    }
}