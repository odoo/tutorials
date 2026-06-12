import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = {
        TodoItem,
    };

    static props = {};

    setup() {
        this.nextId = 1;
        this.state = useState({
            todos: [],
        });

        this.ref = useRef("nameInput");
        onMounted(() => {
            this.ref.el.focus();
        });
    }

    todoCount() {
        this.nextId = this.state.todos.length + 1;
    }

    handleDelete(id) {
        const index = this.state.todos.findIndex((todo) => todo.id === id);
        this.state.todos.splice(index, 1);
        this.state.todos.forEach((todo, index) => {
            todo.id = index + 1;
        });
        this.todoCount()
    }

    toggleState(id) {
        this.state.todos.find(t => t.id === id) ? todo.isCompleted = !todo.isCompleted : ""
    }

    clearAll() {
        this.state.todos = []
    }

    markAll() {
        this.state.todos.filter(t => t.isCompleted == false).forEach((todo) => {
            todo.isCompleted = true
        });
    }


    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value.trim() !== "") {
            this.state.todos.find(t => t.title === ev.target.value.trim()) ? alert("Cant write a duplicate todo")
                : this.state.todos.push({
                    id: this.nextId++,
                    title: ev.target.value.trim(),
                    isCompleted: false,
                });
            ev.target.value = "";
        }
    }
}