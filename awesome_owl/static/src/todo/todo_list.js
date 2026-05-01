import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        this.inputRef = useAutofocus("TodoInput")
        this.toggleTodo = this.toggleTodo.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.key === 'Enter' && ev.target.value.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todoId){
        const todo = this.todos.find(t => t.id === todoId);
        if(todo){
            todo.isCompleted = !todo.isCompleted
        }
    }

    deleteTodo(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
