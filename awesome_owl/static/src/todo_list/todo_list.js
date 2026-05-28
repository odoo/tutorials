import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        this.inputRef = useRef("input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(event) {
        if (event.key === "Enter" && event.target.value.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: event.target.value.trim(),
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === id);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
