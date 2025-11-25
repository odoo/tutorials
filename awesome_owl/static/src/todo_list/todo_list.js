import { Component, useState, useRef } from "@odoo/owl"
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            {id: 1, description: "buy bread", isCompleted: false},
            {id: 2, description: "buy milk", isCompleted: false},
            {id: 3, description: "have lunch", isCompleted: true},
        ]);
        this.todoCounter = this.todos.length;
        this.inputRef = useRef("todo_input")
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input_text = this.inputRef.el.value.trim();
            if (input_text) {
                this.todoCounter++;
                this.todos.push({id: this.todoCounter, description: input_text, isCompleted: false});
                this.inputRef.el.value = "";
            }
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}

