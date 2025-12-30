import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        this.inputRef = useRef("input");
    }
    addTodo(ev) {
        if (ev.keyCode == '13') {
            console.log(ev.target.value)
            if (ev.target.value != "") {
                this.todos.push({
                    id: this.nextId++,
                    description: ev.target.value,
                    isCompleted: false
                })
                ev.target.value = ''
            }
        }
    }
    toggleTodo(id) {
        const todo = this.todos.find(todo => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }
    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
