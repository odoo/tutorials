import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList"
    static components = { TodoItem }
    id = 1;

    setup () {
        this.todos = useState([]);
        useAutoFocus();
    }

    addTask(event) {
        const { target: { value }, keyCode } = event;
        if (keyCode != 13 || !value.trim()) return;
        this.todos.push({
            id: this.id++,
            description: value,
            isCompleted: false,
        });
        event.target.value = '';
    }

    toggleTaskState(todo_id) {
        const task = this.todos.find((t) => t.id === todo_id);
        if (!task) return;
        task.isCompleted = !task.isCompleted;
    }

    taskDelete(todo_id) {
        const taskIndex = this.todos.findIndex((t) => t.id === todo_id)
        if (taskIndex >= 0) {
            this.todos.splice(taskIndex, 1);
        }
    }
}
