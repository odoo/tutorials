import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutoFocus } from "../../utils"

export class TodoList extends Component {
    static template = "awesome_owl.todo.todo_list";

    static components = { TodoItem };

    static props = {};

    setup() {
        this.todos = useState([]);
        this.id = 0;
        useAutoFocus("input");
    }

    addTodo(event) {
        if (event.type !== "keyup" || event.keyCode !== 13 || event.target.value === "") {
            return;
        }
        this.todos.push({id: this.id++, description: event.target.value, isCompleted: false});
        event.target.value = "";
    }

    toggleTodo(id) {
        let todo = this.todos.find(todo => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    #reOrderItems() {
        for (let i = 0; i < this.todos.length; i++) {
            this.todos[i].id = i;
        }
    }

    removeTodo(id) {
        const todo = this.todos.findIndex(todo => todo.id === id);
        this.todos.splice(todo, 1);
        this.#reOrderItems();
        this.id--;
    }
}
