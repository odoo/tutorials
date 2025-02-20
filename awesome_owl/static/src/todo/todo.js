/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { Card } from "../card/card";
import { TodoItems } from "./todo_items";
import { useAutofocus } from "../utils";

export class Todo extends Component {
    static template = "awesome_owl.todo"
    static components = { Card, TodoItems }

    setup() {
        this.todos = useState([])

        const handleKeyUp = (event) => {
            if (event.key === "Enter") {
                if (!event.target.value) {
                    return alert("Empty field not allowed")
                }
                this.todos.push({ id: Math.floor(Math.random() * 1000), description: event.target.value, isCompleted: false });
                event.target.value = ""
            }
        };

        this.handleToggleList = (id) => {
            const todo = this.todos.find((item) => item.id === id);
            if (todo) {
                todo.isCompleted = !todo.isCompleted;
            }
        }

        onMounted(() => {
            document.addEventListener("keyup", handleKeyUp);
        });

        onWillUnmount(() => {
            document.removeEventListener("keyup", handleKeyUp);
        });


        this.deleteTodo = (id) => {
            const index = this.todos.findIndex((elem) => elem.id === id);
            if (index >= 0) {
                this.todos.splice(index, 1);
            }
        }

        useAutofocus('task_input')

    }

}
