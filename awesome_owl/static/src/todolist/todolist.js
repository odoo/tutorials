/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils/utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup() {
        this.inputRef = useAutofocus("input")
        this.todoTasks = useState([
            { id: 1, description: "watering plants", isCompleted: true },
            { id: 2, description: "write tutorial", isCompleted: true },
            { id: 3, description: "buy milk", isCompleted: false }
        ]);
        this.todoCounter = useState({ value: 4 });
    }

    addTodo = (ev) => {
        if (ev.keyCode === 13 && ev.target.value != '') {
            this.todoTasks.push({ id: this.todoCounter.value, description: ev.target.value, isCompleted: false });
            this.todoCounter.value++;
            ev.target.value = "";
        }
    }

    toggleTaskState(id) {
        const toggleTask = this.todoTasks.find(task => task.id === id);
        if (toggleTask) {
            toggleTask.isCompleted = !toggleTask.isCompleted
        }
    }

    removeTodoTask(id) {
        const index = this.todoTasks.findIndex((task) => task.id === id);
        if (index >= 0) {
            this.todoTasks.splice(index, 1);
        }
    }

}
