import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static counter = 0;
    
    setup() {
        this.todos = useState([]);
        this.state = useState({ newTodo: "" });
        this.inputRef = useAutofocus("input_focus");
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && this.state.newTodo.trim() !== "") {
            this.todos.push({ id: TodoList.counter++, description: this.state.newTodo, isCompleted: false });
            this.state.newTodo = "";
        }
    }

    toggleCompleted(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
           this.todos.splice(index, 1);
        }
    }
}
