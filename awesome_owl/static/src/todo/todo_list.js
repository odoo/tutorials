import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todo_item";
import { Autofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.nextId = 0;
        this.todos = useState([]);
        Autofocus("input")
    }

    addTodo(event) {
        if (event.key === 'Enter' && event.target.value !== '') {
            this.todos.push({
                id: this.nextId++,
                description: event.target.value,
                isCompleted: false
            });

            event.target.value = '';
        }
    }

    listToggleComplete(itemId) {
        const todoItem = this.todos.find(item => item.id === itemId);
        if (todoItem) {
            todoItem.isCompleted = !todoItem.isCompleted;
        }
    }

    removeTodo(itemId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === itemId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
