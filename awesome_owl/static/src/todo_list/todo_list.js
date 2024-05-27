/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.tasks = useState([]);
        useAutofocus('task_input');
    }

    onKeyup(event) {
        // Add task
        if (event.keyCode === 13) {
            const lastTask = this.tasks[this.tasks.length - 1];
            const nextAvailableId = lastTask ? lastTask.id + 1 : 0;
            this.tasks.push({id: nextAvailableId, description: event.target.value, isCompleted: false});
            event.target.value = '';
        }
    }

    setCompleted(id, completed) {
        const task = this.tasks.find(task => task.id === id);
        if (task) {
            task.isCompleted = completed;
        }
    }

    deleteTask(id) {
        const taskIndex = this.tasks.findIndex(task => task.id === id);
        if (taskIndex >= 0) {
            this.tasks.splice(taskIndex, 1);
        }
    }
}
