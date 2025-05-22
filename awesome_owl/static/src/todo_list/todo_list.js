import { Component, useState, onWillStart } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";
import { TodoModel } from "./todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todoModel = new TodoModel();
        onWillStart(() => {
            return this.todoModel.load();
        });
        useAutofocus("input")
    }

    handleKeypress(ev) {
        if (ev.key === "Enter") {
            const input = ev.target;
            if (input.value.trim()) {
                this.todoModel.createTodo(input.value);
                input.value = "";
            }
        }
    }

    createTask() {
        const input = this.refs.input;
        if (input.value.trim()) {
            this.todoModel.createTodo(input.value);
            input.value = "";
        }
        input.focus();
    }
}
