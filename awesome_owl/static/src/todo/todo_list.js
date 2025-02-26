import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "@awesome_owl/utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [],
            newTask: "",
        });
        this.nextId = 1;
        this.inputRef = useAutofocus("taskInput");
    }

    onTodoToggle(todo) {
        console.log(`Todo ${todo.id} toggled to ${todo.isCompleted}`);
    }
    static props = {};

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = this.state.newTask.trim();
            if (description) {
                this.state.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });
                this.state.newTask = "";
            }
        }
    }
}
