import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutofocus } from "./utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [],
            newTask: '',
        });

        this.inputRef = useAutofocus(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            if (this.state.newTask.trim() !== "") {
                const newTodo = {
                    id: this.state.todos.length + 1,
                    description: this.state.newTask,
                    isCompleted: false
                };
                this.state.todos = [...this.state.todos, newTodo];
                this.state.newTask = '';

                this.inputRef.el.focus();
            }
        }
    }
}
