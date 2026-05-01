import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const value = ev.target.value.trim();
            if (!value) return;
            this.todos.push({
                id: this.nextId++,
                description: value,
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
        }
    }
}
