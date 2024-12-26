import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        this.input = useAutofocus("todo_input");
    }

    addTodo(event) {
        if(event.keyCode === 13) {
            const inputValue = event.target.value;
            if(inputValue.trim() === "") return;
            
            const lastTodo = this.todos[this.todos.length - 1];
            let newId = lastTodo === undefined ? 0 : lastTodo.id + 1;

            this.todos.push({
                id: newId,
                description: inputValue,
                isCompleted: false
            });
            event.target.value = "";
        }
    }

    toggleTodo(id) {
        const todoItem = this.todos.find(todo => todo.id === id);
        if(todoItem !== undefined) {
            todoItem.isCompleted = !todoItem.isCompleted;
        }
    }

    removeTodo(id) {
        const todoItemIndex = this.todos.findIndex(todo => todo.id === id);
        if(todoItemIndex >= 0) {
            this.todos.splice(todoItemIndex, 1);
        }
    }
}
