import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        this.state = useState({
            inputValue: ""
        });
        this.inputTodo = useRef('inputTodo');
        onMounted(() => {
            this.inputTodo.el.focus()
        })
    }

    addTodo(event) {
        if (event.keyCode !== 13 | this.state.inputValue === "") return;

        this.todos.push({
            id: this.todos.length,
            description: this.state.inputValue,
            isCompleted: false
        })

        this.state.inputValue = "";

    }

    removeTodo(id) {
        const idx = this.todos.findIndex(todo => todo.id === id)
        if (idx !== -1) {
            this.todos.splice(idx, 1)
        }
    }
}