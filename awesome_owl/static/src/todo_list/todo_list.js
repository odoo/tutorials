import { Component, useState, useRef } from "@odoo/owl";
import { ToDoItem } from "./todo_item";
import { Utils } from "../utils";


export class ToDoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = {ToDoItem};

    setup() {
        this.todos = useState([]);
        this.todoCounter = 1;
        this.inputRef = useRef('input');
        Utils.useAutofocus(this.inputRef);
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();
            if (description) {
                this.todos.push({
                    id: this.todoCounter++,
                    description: description,
                });
                input.value = "";
            }
        }
    }

    toggleState(todoItemId) {
        const todo = this.todos.find((todo) => todo.id === todoItemId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    onDelete(todoItemId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoItemId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
