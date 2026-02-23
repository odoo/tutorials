import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static props = [];
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "drink water", isCompleted: true },
            { id: 2, description: "do tutorial", isCompleted: false },
            { id: 3, description: "sleep", isCompleted: false },
        ]);
        this.count = this.todos.length;
        useAutofocus("input");
    }

    addTodo(event) {
        if (event.keyCode == 13 && event.target.value != "") {
            this.todos.push({
                id: ++this.count,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index != -1) {
            this.todos.splice(index, 1);
        }
    }
}
