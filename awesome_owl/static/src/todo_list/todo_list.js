import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static props = {
        items: { type: Array, optional: true },
    };
    static components = {
        TodoItem,
    };
    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef("todo_input");
        onMounted(() => {
            if (this.inputRef.el) this.inputRef.el.focus();
        });
    }
    addTodo(ev) {
        if (ev.key === "Enter") {
            const value = ev.target.value.trim();

            if (!value) {
                return;
            }

            this.todos.push({
                id: this.nextId++,
                description: value,
                isCompleted: false,
            });

            ev.target.value = "";
        }
    }

    toggleState(id, value) {
        const todo = this.todos.find((t) => t.id === id);
        if (todo) {
            todo.isCompleted = value;
        }
        console.log(this.todos);
    }

    deleteItem(id) {
        const index = this.todos.findIndex((t) => t.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
