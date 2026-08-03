import { Component, useState, useRef, onMounted } from "@odoo/owl"
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList"
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef("input");

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();

            this.todos.push({
                id: this.nextId++,
                description: description,
                // isCompleted: false,
            });

            ev.target.value = "";
        }
    }
}
