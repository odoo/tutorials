import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"
import { useAutoFocus } from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }
    
    setup() {
        this.todos = useState([]);
        useAutoFocus("inputTodo");
        this.index = 0;
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    }

    addTodo(event) {
        if (event.target.value.trim() && event.keyCode === 13) {
            this.todos.push({
                id: ++this.index,
                description: event.target.value,
                isCompleted: false
            });
            event.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(todo => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if(index != -1) {
            this.todos.splice(index, 1);
        }
    }
}
