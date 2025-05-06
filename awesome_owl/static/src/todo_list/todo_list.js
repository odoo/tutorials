import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { Todo } from "./todo";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.length = useState({ value: 0 });
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value) {
            this.length.value++;
            this.todos.push(new Todo(ev.target.value, this.length.value));
            ev.target.value = "";
        }
    }

    removeTodo(elemId) {
        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            this.todos.splice(index, 1);
            this.length.value--;
            for (let i = 0; i < this.length.value; i++) {
                this.todos[i].index = i + 1;
            }
        }
    }
}
