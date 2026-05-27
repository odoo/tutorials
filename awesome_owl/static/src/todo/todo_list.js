import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.items = useState([{ id: 1, description: "Buy milk", isCompleted: true }]);
        this.nextId = 2;
        this.inputRef = useRef("input");

        onMounted(() => {
            if (this.inputRef.el) this.inputRef.el.focus();
        });
    }

    createItem(ev) {
        if (ev.key === "Enter") {
            const description = ev.target.value.trim();

            if (!description) {
                return;
            }

            this.items.push({
                id: this.nextId++,
                description: description,
                isCompleted: false
            });

            ev.target.value = "";
        }
    }

    toggleItem(item_id) {
        const todo = this.items.find(t => t.id === item_id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteItem(item_id) {
        const index = this.items.findIndex((t) => t.id === item_id);
        if (index >= 0) {
            this.items.splice(index, 1);
        }
    }
}
