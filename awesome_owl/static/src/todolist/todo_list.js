import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";    

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static props = {
        addTodo : {type: Function, optional: true }
    };

    setup() {
        this.todos = useState([]);
        this.todoId = 1;
        this.inputRef = useAutofocus('input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();
            if (description) {
                this.todos.push({
                    id: this.todoId++,
                    description,
                    isCompleted: false,
                });
                input.value = "";
            }
        }
    }

    toggleTodoState(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
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
