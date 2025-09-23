import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        useAutoFocus("todo-input");
        this.state = useState({todos: {
                1: { description: "buy milk", isCompleted: false }, 
                2: { description: "buy tomatoes", isCompleted: true }
            },
            lastId: 2
        });
    }

    toggleState(id) {
        this.state.todos[id].isCompleted = !this.state.todos[id].isCompleted;
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.state.todos[++this.state.lastId] = {description: ev.target.value, isCompleted: false};
            ev.target.value = "";
        }
    }

    removeTodo(id) {
        delete this.state.todos[id];
    }
}
