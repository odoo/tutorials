import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.todos = useState([]);
        useAutofocus("add_todo_input");
    }

    addToDo(event) {
        if (event.keyCode === 13 && event.target.value !== "") {
            this.todos.push({id: this.todos.length, description: event.target.value, isCompleted: false});
            event.target.value = "";
        }
    }
}
