import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item/todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [],
        });
        this.addTodo = this.addTodo.bind(this);
        this.toggleTodo = this.toggleTodo.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            const newId =
                this.state.todos.length > 0
                    ? Math.max(...this.state.todos.map((todo) => todo.id)) + 1
                    : 1;
            this.state.todos.push({
                id: newId,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.state.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.state.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }
}
