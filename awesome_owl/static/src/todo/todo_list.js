import { Component, markup, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils"

export class TodoList extends Component {
    static components = {
        TodoItem,
    };

    static template = "awesome_owl.todo_list";

    setup() {
        this.todos = useState([]);
        useAutofocus('todo_input');
        this.nextId = 0;
    }

    createTodo = (ev) => {
        if (ev.keyCode != 13)
            return;

        const text = ev.target.value.trim();

        if (!text)
            return;

        this.todos.push({
            id: ++this.nextId,
            description: text,
            isCompleted: false,
        });

        ev.target.value = "";
    }

    handleTodoStateChanged = (todoId) => {
        const toChange = this.todos.find(t => t.id == todoId);
        toChange.isCompleted = !toChange.isCompleted;
    }

    handleDeleteTodo = (todoId) => {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
