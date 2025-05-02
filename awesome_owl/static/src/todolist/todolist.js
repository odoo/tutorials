import { useRef, useState, onMounted, Component } from "@odoo/owl";

import { useAutofocus } from "./../utils";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.state = useState({ counter: 0 });
        this.inputRef = useRef("task_name");
        onMounted(() => {
            useAutofocus(this.inputRef);
        });
    }

    removeTodo(todoId) {
        this.todos.splice(todoId, 1);

        // Reindex all the next ids
        for (; todoId < this.todos.length; todoId++) {
            this.todos[todoId].id = todoId;
        }
    }

    addTodo(event) {
        if (event.keyCode === 13 && this.inputRef.el.value !== "") {
            this.todos.push({
                id: this.state.counter,
                description: this.inputRef.el.value,
                isCompleted: false,
            });
            this.state.counter++;
            this.inputRef.el.value = "";
        }
    }
}
