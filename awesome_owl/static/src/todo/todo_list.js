import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef("newTodoInput");
    }
    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = this.inputRef.el.value.trim();
            if (!description) return;
            this.todos.push({
                id: this.nextId++,
                description,
                isCompleted: false,
            });
            this.inputRef.el.value = "";
        }
    }
}