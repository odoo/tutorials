import { Component, useState } from "@odoo/owl";
import { useFocus } from "../utils";
import { TodoItem } from "./todo_item";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([]);
        this.id = 1;
        useFocus("input");

    }

    addTodo(input) {
        if (input.keyCode !== 13 || input.target.value == "") {
            return;
        }

        const todo = {
            id: this.id,
            description: input.target.value,
            isCompleted: false,
        }

        this.todos.push(todo);
        input.target.value = "";
        this.id++;
    }

    removeTodo(idDelete) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === idDelete)
        this.todos.splice(todoIndex, 1)
    }

}