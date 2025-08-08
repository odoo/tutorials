import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem }

    setup() {
        this.state = useState({ todos: [], id: 0 });
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo =  this.removeTodo.bind(this);

        useAutoFocus('inputRef');
    }

    addToTodo(ev) {
        const description = ev.target.value.trim();
        if (ev.keyCode === 13 && description !== "") {
            this.state.todos.push({
                id: this.state.id,
                description: description,
                isCompleted: false
            });
            this.state.id++;
            ev.target.value = "";
        }
    }

    toggleState(id, isChecked) {
        const todo = this.state.todos.find(todo => todo.id === id);
        if (todo) {
            todo.isCompleted = isChecked;
        }
    }

    removeTodo(id) {
        const index = this.state.todos.findIndex(todo => todo.id === id);

        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }

}
