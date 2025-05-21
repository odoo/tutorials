import {Component, useState, useRef, onMounted} from "@odoo/owl";
import {TodoItem} from "./todo_item";
import {useCustomAutofocus} from "../util";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static props = {}
    static components = {TodoItem};

    newtTodoId = 1;

    setup() {
        this.state = useState({todos: [], newTodo: ""});
        useCustomAutofocus("todoInput")
        this.toggleTodoState = this.toggleTodoState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);

    }

    addTodo(ev) {
        if (ev.keyCode !== 13 || !this.state.newTodo) {
            return;
        }

        const todoItem = {
            id: this.newtTodoId++,
            description: this.state.newTodo,
            isCompleted: false
        }
        this.state.newTodo = ""
        this.state.todos.push(todoItem)
    }

    toggleTodoState(todoId) {
        const todo = this.state.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodo(todoId) {
        const index = this.state.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }

}
