import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    
    setup() {
        this.todos = useState([]);
        this.nextId = useState({value: 0});
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.todos.push({ id: this.nextId.value++, description: ev.target.value, isCompleted: false });
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            this.todos[index].isCompleted = !this.todos[index].isCompleted;
        }
    }

    delete(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
