import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        useAutofocus('input');
    }

    counter = 0;

    addTodoItem(ev) {
        const description = ev.target.value.trim();
        if (ev.keyCode === 13 && description) {
            this.todos.push({ 'id': this.counter, 'description': description, 'isCompleted': false });
            ev.target.value = "";
            this.counter++;
        }
    }

    toggleState(id) {
        const itemToUpdate = this.todos.find(item => item.id === id);

        if (itemToUpdate) {
            itemToUpdate.isCompleted = !itemToUpdate.isCompleted;
        }
    }

    removeTodoIteam(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index,1);
        }
    }
}
