import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    setup() {
        this.inputRef = useRef("todoInput");
        this.todos = useState([]);
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(event) {
        if (event.key === "Enter") {
            if (!event.target.value) {
                return;
            }
            this.todos.push({
                id: this.todos.length + 1,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    removeTodo = (todoId) => {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    };

    static components = { TodoItem };
}
