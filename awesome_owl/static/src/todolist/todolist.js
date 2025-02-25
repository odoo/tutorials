import { Component, useState } from "@odoo/owl";
import { ToDoItem }  from "./todoitem";
import { useAutofocus } from "../util.js";

export class ToDoList extends Component {
    static template = "awesome_owl.ToDoList";
    static components = { ToDoItem };

    setup() {
        this.ids = 1;
        this.todos = useState([]);
        useAutofocus("inputAddTodo")
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value != ''){
            this.todos.push({
                id: this.ids++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find((t) => t.id === id);
        if(todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const todo = this.todos.findIndex((t) => t.id === id);
        if (todo >= 0) {
          this.todos.splice(todo, 1);
        }
    }
}   