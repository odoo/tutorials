import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils/utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: []
        });

        this.inputRef = useAutoFocus("todo_input");

        this.idCount = 0;
    }

    addTodo(ev) {
        const description = ev.target.value.trim();
        if (ev.keyCode === 13 && description) {
            const newTodo = {
                id: this.idCount++,
                description: description,
                isCompleted: false
            };
            this.state.todos.push(newTodo);
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.state.todos.find(todo => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        this.state.todos = this.state.todos.filter(todo => todo.id !== id);
    }
}