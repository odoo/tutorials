/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef('input');
        // Focuse the input when the component is mounted
        onMounted(() => {
            this.inputRef.el.focus();
        });

        // Use the useAutofocus hook to focus the input
        this.inputRef = useAutofocus('input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            let input = ev.target;
            let description = input.value.trim();
            if (description !== "") {
                this.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });
                input.value = ""; 
            }
        }
    }
}
