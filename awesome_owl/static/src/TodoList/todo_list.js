import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from '../utils';

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem}
    static props = {}

    setup() {
        this.todos = useState([]);
        this.todoId = useState([1]);
        useAutofocus('bestInputEver');
    }

    createTodo = (e) => {
        if (e.keyCode === 13 && e.target.value) {
            this.todos.push({id: this.todoId++, description: e.target.value, isCompleted: false})
            e.target.value = "";
        }
    }

    toggleState = (id) => {
        const todo = this.todos.filter(t => t.id === id)[0];
        todo.isCompleted = !todo.isCompleted;
        console.log(todo);
    }

    removeTodo = (id) => {
        const index = this.todos.findIndex(t => t.id === id)
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
