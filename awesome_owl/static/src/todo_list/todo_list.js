import { Component, useState, onWillStart } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";
import { TodoModel } from "./todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.model = new TodoModel();
        onWillStart(() => {
            return this.model.load();
        });
        useAutofocus("input")
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const input = ev.target;
            this.model.createTodo(input.value);
            input.value = "";
        }
    }

    addTodoBtn() {
        const input = this.refs.input;
        if (input.value.trim()) {
            this.model.createTodo(input.value);
            input.value = "";
        }
        input.focus();
    }
}
