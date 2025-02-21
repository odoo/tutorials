import { Component, useState, useRef, onMounted } from "@odoo/owl";

import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static components = { TodoItem };
    static template = "awesome_owl.TodoList";

    setup() {
        this.todos = useState([
            { id: 1, description: "Buy groceries", isCompleted: false }
        ]);

        this.inputRef = useRef('input');
        onMounted(() => {
            this.inputRef.el.focus();
        });

        this.toggleTodoState = this.toggleTodoState.bind(this);
        this.removeTodoState = this.removeTodoState.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value;
            if (description) {
                this.todos.push({ id: this.todos.at(-1).id + 1, description, isCompleted: false });
                ev.target.value = "";
            }
        }
    }

    toggleTodoState(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodoState(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
