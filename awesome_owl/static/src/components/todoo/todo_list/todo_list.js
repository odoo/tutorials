import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../../../utils";
export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    setup() {
        this.todos = useState([]);
        useAutofocus("todo_input");
    }
    addTodo(event) {
        if (event.keyCode === 13 && event.target.value.length) {
            this.todos.push({
                id: this.todos.length
                    ? this.todos[this.todos.length - 1].id + 1
                    : 1,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }
    toggleState(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
