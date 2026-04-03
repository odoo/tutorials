import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        useAutofocus("inputRef")
    }

    addTodo(ev) {
        if(ev.keyCode === 13) {
            const taskName = ev.target.value.trim();

            if(taskName !== ""){
                this.todos.push({
                    id: this.nextId++,
                    description: taskName,
                    isCompleted: false,
                });

                ev.target.value = "";
            }
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
    
}
