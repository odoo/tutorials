import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    setup() {
        this.todos = useState([]);
        this.counter = 0
        this.inputRef = useAutoFocus("todo_input_ref")
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value !== "") {
            this.todos.push({
                id: ++this.counter,
                description: event.target.value,
                isCompleted: false
            })
            event.target.value = ""
        }
    }

    toggleState(id) {
        if (id) {
            const toUpdate = this.todos.find(todo => todo.id === id)
            if (toUpdate) {
                toUpdate.isCompleted = !toUpdate.isCompleted
            }
        }
    }

    removeTodo(id) {
        if (id) {
            const index = this.todos.findIndex(todo => todo.id === id)
            this.todos.splice(index, 1)
        }
    }

    static components = { TodoItem }
}
