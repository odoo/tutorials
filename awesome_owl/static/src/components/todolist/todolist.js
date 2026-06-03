import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = {
        TodoItem,
    };

    static props = {};

    setup() {
        this.nextId = 1;

        this.state = useState({
            todos: [],
        });

        this.ref = useRef("nameInput");
        onMounted(() => {

            console.log(this.ref.el);

            this.ref.el.focus();

        });
    }


    handleDelete(id) {
        this.state.todos = this.state.todos.filter(
            t => t.id !== id
        )
    }
    toggleState(id) {
        const todo = this.state.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    onKeydown(ev) {

        if (ev.key === "Enter") {

            const title = ev.target.value.trim();

            if (!title) {
                return;
            }

            this.state.todos.push({
                id: this.nextId++,
                title: title,
                isCompleted: false,
            });

            ev.target.value = "";
        }
    }
}