import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef("todoInput");

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const description = ev.target.value.trim();
            debugger;
            if (!description) return;
            this.todos.push({
                id: this.nextId++,
                description: description,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
            this.todos.forEach((todo, idx) => {
            todo.id = idx + 1;
            });
            this.nextId = this.todos.length + 1;
        }
    }
}
