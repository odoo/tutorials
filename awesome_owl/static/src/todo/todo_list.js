import {Component, onMounted, toRaw, useRef, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    numOfItems = 1;

    setup() {
        this.todos = useState([]);
        this.state = useState({description: ""});

        this.addItem = this.addItem.bind(this);
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);

        useAutoFocus("input");
    }

    addItem(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push(
                {
                    id: this.numOfItems++,
                    description: ev.target.value,
                    isCompleted: false,
                }
            );
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos[index].isCompleted = !this.todos[index].isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
