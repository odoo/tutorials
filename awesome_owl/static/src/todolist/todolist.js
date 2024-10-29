import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem/todoitem";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = 'awesome_owl.todolist';

    static components = { TodoItem };

    setup() {
        this.state = useState({ id: 2, newTodo: '', todos: [{ id: 1, description: "Meow", isCompleted: true }] })
        this.inputRef = useAutoFocus('focus_text');
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    };

    addTodo(ev) {
        if (ev.keyCode === 13 && this.state.newTodo.length > 0) {
            this.state.todos.push({id: this.state.id++, description: this.state.newTodo, isCompleted: false});
            this.state.newTodo = '';
        }
    }

    toggleState(todoId) {
        const index = this.state.todos.findIndex((elem) => elem.id === todoId);
        this.state.todos[index].isCompleted = !this.state.todos[index].isCompleted;
    }

    removeTodo(todoId) {
        const index = this.state.todos.findIndex((elem) => elem.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }
}
