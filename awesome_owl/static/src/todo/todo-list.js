import { useState, Component } from "@odoo/owl";
import { TodoItem } from "./todo-item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo-list";
    static components = { TodoItem };

    setup() {
        this.state = useState({ todos: [], nextId: 1 });
        useAutoFocus("new-todo-input");
    }

    input_event_handler(event) {
        // keyCode is deprecated, use key instead
        if (event.key === "Enter") {
            if (event.target.value) {
                this.state.todos.push({
                    id: this.state.nextId,
                    description: event.target.value,
                    isCompleted: false,
                });
                this.state.nextId++;
                event.target.value = "";
            }
        }
    }

    toggleState(todoId) {
        const selectedTodo = this.state.todos.find((todo) => todo.id === todoId);
        if (selectedTodo) {
            selectedTodo.isCompleted = !selectedTodo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.state.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }
}
