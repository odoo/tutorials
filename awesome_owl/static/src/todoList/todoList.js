import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todoItem/todoItem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo.list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.newTodo = useState({ newDescription : "", nextId : 1});
        useAutofocus("autofocus");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && this.newTodo.newDescription.trim()) {
            this.todos.push({ id: this.newTodo.nextId, description : this.newTodo.newDescription, isCompleted : false });
            this.newTodo.nextId++;
            this.newTodo.newDescription = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(todo => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id){
        const index = this.todos.findIndex(elem => elem.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
      }
    }
}
