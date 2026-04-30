import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([]);
        this.inputRef = useRef("todoInput");
        this.nextId = 1;
    }

    addTodo(ev) {

        if (ev.keyCode === 13 ) {

            const description = ev.target.value.trim();

            if (description !== "") {
                this.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });

                ev.target.value = "";
                
            }
        }
    }
}