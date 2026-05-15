import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.idCount = 0;
        this.todos = useState([]);
        useAutofocus("todolist-input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() != "") {
            this.todos.push({
                id: this.idCount++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
}
