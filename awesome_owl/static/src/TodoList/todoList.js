import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "../TodoItem/todoItem";
import { useAutofocus } from "@web/core/utils/hooks";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.todo_id = 0;
        this.inputRef = useRef('input');
        useAutofocus({ refName: "input" });
        this.onToggle = this.onToggle.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    }

    addData(ev) {
        if (ev.key === 'Enter') {
            const value = ev.target.value.trim();
            if (!value) return;

            this.todos.push({
                id: this.todo_id++,
                description: value,
                isCompleted: false,
            });

            ev.target.value = "";
        }
    }

    onToggle(id) {
        let todo = this.todos[id];
        todo.isCompleted = !todo.isCompleted
    }

    removeTodo(id) {
        this.todos.splice(id, 1);
        this.todo_id = 0
        for (const todo of this.todos) (
            todo.id = this.todo_id++
        )
    }
}
