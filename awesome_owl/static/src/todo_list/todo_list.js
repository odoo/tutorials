import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        useAutoFocus("todo-input");
        this.state = useState({todos: {
                2: { description: "penser à acheter du lait", isCompleted: false }, 
                3: { description: "penser à acheter des tomates cerises", isCompleted: true }
            },
            lastId: 3
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
