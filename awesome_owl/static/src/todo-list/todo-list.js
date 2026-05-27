import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo-item/todo-item";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        this.inputRef = useRef("input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    toggleState(id) {
        const todo = this.todos.find((t) => t.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex((t) => t.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value;
            if (description) {
                this.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });
                ev.target.value = "";
            }
        }
    }
}