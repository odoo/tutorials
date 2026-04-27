import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.todos = useState([]);
    }

    addToDo(event) {
        if (event.keyCode === 13 && event.target.value !== "") {
            this.todos.push({id: this.todos.length, description: event.target.value, isCompleted: false});
            event.target.value = "";
        }
    }
}
