import {Component, useState, onMounted, useRef} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.todos = useState([{id: 1, description: "abcd", isCompleted: true}, {
            id: 2,
            description: "abcd",
            isCompleted: false
        },]);
        // this.inputRef = useAutofocus("input");
        this.taskInput = useRef("taskInput");
        onMounted(() => {
            this.taskInput.el.focus();
        });


    }

    toggleState(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    addTodo(ev) {
        if (ev.key !== "Enter") {
            return;
        }

        const description = ev.target.value.trim();

        if (!description) {
            return;
        }

        this.todos.push({
            id: Math.max(0, ...this.todos.map(todo => todo.id)) + 1, description: description, isCompleted: false,
        });

        ev.target.value = "";
    }
}
