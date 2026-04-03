import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";

export class Todo extends Component {

    static template = "awesome_owl.Todo";

    static components = { TodoItem };

    setup() {

        this.state = useState({
            tasks: []
        });

        this.nextId = 1;

        this.inputRef = useRef("taskInput");

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTask(ev) {

        if (ev.key === "Enter") {

            const value = ev.target.value.trim();

            if (!value) return;

            this.state.tasks.push({
                id: this.nextId++,
                name: value,
                isCompleted: false
            });

            ev.target.value = "";
        }
    }

    toggleState(id) {

        const task = this.state.tasks.find(t => t.id === id);

        if (task) {
            task.isCompleted = !task.isCompleted;
        }
    }

    deleteTask(id) {
        this.state.tasks = this.state.tasks.filter(task => task.id !== id);
    }

    get remainingTasks() {
        return this.state.tasks.filter(task => !task.isCompleted).length;
    }

}
