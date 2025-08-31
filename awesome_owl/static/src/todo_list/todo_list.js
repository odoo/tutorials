import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.counter = 1;
        useAutofocus("todo_input");
    }

    addTodo (event) {
        const description = event.target.value
        if (event.keyCode === 13 && description !== "") {
            this.todos.push({
                id: this.counter,
                description: description,
                isCompleted: false,
            });
            this.counter++;
            event.target.value = ""
        }
    }

    toggleState (id) {
        const todo = this.todos.find(item => item.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo (id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
