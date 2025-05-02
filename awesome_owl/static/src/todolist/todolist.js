/** @odoo-module **/

import { useRef, useState, onMounted, Component } from "@odoo/owl";

import { useAutofocus } from "./../utils";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    
    todos = useState([]);
    state = useState({ counter: 0 });

    setup() {
        this.inputRef = useRef("task_name");
        onMounted(() => {
            useAutofocus(this.inputRef);
        });
    }

    addTodo(event) {
        if (event.keyCode === 13 && this.inputRef.el.value !== "") {
            this.todos.push({
                id: this.state.counter,
                description: this.inputRef.el.value,
                isCompleted: false,
            });
            this.state.counter++;
        }
    }
}
