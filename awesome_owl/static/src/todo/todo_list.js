import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {

    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef("todo_input")

        onMounted(() => {
            this.inputRef.el.focus()
        })
    }

    addTodo(e) {
        if (e.keyCode !== 13) {
            return;
        }

        const value = e.target.value.trim();

        if (!value) {
            return;
        }

        this.todos.push({
            id: this.nextId++,
            description: value,
            isCompleted: false,
        });
        e.target.value = "";
        this.inputRef.el.focus()
    }

    toggleState = (todoId) => {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    };

    removeTodo = (todoId) => {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    };
}
