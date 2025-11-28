import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: true },
            { id: 2, description: "clean room", isCompleted: false },
            { id: 3, description: "go to the gym", isCompleted: false },
        ]);
        this.inputRef = useAutofocus("add-input");
    }

    toggleState = (todoId) => {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim()) {
            const newId = this.todos.length > 0 ? Math.max(...this.todos.map(t => t.id)) + 1 : 1;
            this.todos.push({
                id: newId,
                description: ev.target.value.trim(),
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    removeTodo = (todoId) => {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
