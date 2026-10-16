import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            {
                id: 1,
                description: "This is my first todo",
                isCompleted: true
            },
            {
                id: 2,
                description: "This is my second todo",
                isCompleted: false
            },
        ]);

        this.inputRef = useRef("todo-input")

        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    addTodo(ev) {
        if (ev.key !== "Enter") {
            return;
        }

        const description = ev.target.value.trim();

        if (!description) {
            return;
        }

        this.todos.push({
            id: Math.max(0, ...this.todos.map(todo => todo.id)) + 1,
            description: description,
            isCompleted: false,
        });

        ev.target.value = "";
    }

    toggleTodoState(id) {
        const todo = this.todos.find((todo) => todo.id === id);

        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const todoIndex = this.todos.findIndex(todo => todo.id === id);

        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
