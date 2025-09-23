import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        useAutofocus("todoInput");
    }

    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value.trim() !== "") {
            this.todos.push({
                id: this.todos.length + 1,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    setTodoCompletion(todo, ev) {
        if (ev.target.checked != todo.isCompleted) {
            todo.isCompleted = ev.target.checked;
        }
    }
}
