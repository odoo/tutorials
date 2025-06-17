import { Component, useRef, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static components = { TodoItem };

    static template = "awesome_owl.todolist";

    static props = {};

    setup() {
        this.id = 1; // could be calculated every iteration but would get very slow with a lot of todos
        this.todos = useState([
            // removed following 9. Adding a todo
            // { id: 2, description: "write tutorial", isCompleted: true },
            // { id: 3, description: "buy milk", isCompleted: false },
        ]);
        this.inputRef = useRef("addTask");
        useAutofocus("addTask");
    }

    addTodo(ev) {
        if (ev.keyCode != 13 || !this.inputRef.el) {
            return;
        }

        const desc = this.inputRef.el.value;

        if (desc === "") {
            return;
        }

        this.todos.push({
            id: this.id,
            description: desc,
            isCompleted: false,
        });

        this.inputRef.el.value = "";
        this.id++;
    }

    removeTodo(elemId) {
        if (elemId < 0 || elemId >= this.id) {
            return;
        }

        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }
}
