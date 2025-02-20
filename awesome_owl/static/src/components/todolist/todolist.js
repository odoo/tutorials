import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";
import { useAutofocus } from "../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    setup() {
        this.counterId = useState({ value: 1 });
        this.todos = useState({ value: [] });
        this.newTask = useState({ value: "" });
        this.toggleIsCompleted = this.toggleIsCompleted.bind(this);
        this.inputRef = useAutofocus("inref");
        this.deleteTodo = this.deleteTodo.bind(this);
    }
    addTask() {
        if (this.newTask.value.trim()) {
            const newTodo = {
                id: this.counterId.value,
                description: this.newTask.value.trim(),
                isCompleted: false,
            };
            this.todos.value = [...this.todos.value, newTodo];
            this.counterId.value++;
            this.newTask.value = "";
        }
        this.inputRef.el.focus();
    }
    keyPress(ev) {
        if (ev.keyCode === 13) {
            this.addTask();
        }
    }
    toggleIsCompleted(id) {
        this.todos.value = this.todos.value.map((t) => {
            if (t.id === id) {
                t.isCompleted = !t.isCompleted;
            }
            return t;
        });
    }
    deleteTodo(id) {
        this.todos.value = this.todos.value.filter((t) => t.id != id);
    }
    static components = { TodoItem };
}
