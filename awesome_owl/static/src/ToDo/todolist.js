import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.counter = 0;
        useAutofocus("input");
    }

    addTodo(event) {
        if (event.keyCode == 13 && event.target.value != "") {
            this.todos.push({
                id: this.counter++,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find(todo => todo.id == todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    

    removeTodo(todoId) {
        const index = this.todos.findIndex(todo => todo.id == todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
