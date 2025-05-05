import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { Todo } from "./todo";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push(new Todo(ev.target.value));
            ev.target.value = "";
        }
    }

    removeTodo(elemId) {
        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
