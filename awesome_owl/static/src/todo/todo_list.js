import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        useAutoFocus("todoInput");
    };

    addTodo(ev) {
        const description = ev.target.value;
        if (ev.keyCode === 13 && description.length > 0) {
            const newTodo = {
                id: this.todos.length + 1,
                description: description,
                isCompleted: false,
            };
            this.todos.push(newTodo);
            ev.target.value = "";
        }
    };

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    };
    
    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    };
}
