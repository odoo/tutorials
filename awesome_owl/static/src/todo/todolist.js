import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useAutofocus('inputRef');  //
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();
            if (description !== "") {
                this.todos.push({
                    id: this.nextId++,
                    description,
                    isCompleted: false
                });
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

    removeTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
