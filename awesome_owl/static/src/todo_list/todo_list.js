
import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "./utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        useAutoFocus("focus_input")
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value.trim()) {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            })

            ev.target.value = ""
        }
    }

    toggleState(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if(todo){
            this.todos[id].isCompleted = !this.todos[id].isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if(index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
