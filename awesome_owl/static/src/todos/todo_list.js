import { useState, Component, useRef } from "@odoo/owl"
import { TodoItem } from "./todo_item"
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"

    setup() {
        this.inputRef = useRef('inputRef')
        this.state = useState([{
            id: 0,
            isCompleted: true,
            description: "test description"
        }]);

        useAutoFocus(this.inputRef)
        this.toggleState = this.toggleState.bind(this)
        this.removeTodo = this.removeTodo.bind(this)
        this.current_id = 1
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value !== "") {
            this.state.unshift({
                id: this.current_id,
                description: e.target.value,
                isCompleted: false
            })
            this.inputRef.el.value = ""
            this.current_id++
        }
    }

    removeTodo(id) {
        const index = this.state.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.state.splice(index, 1);
        }
    }

    toggleState(id) {
        const current_todo = this.state.find((todo) => todo.id == id)
        if (current_todo) {
            current_todo.isCompleted = !current_todo.isCompleted
        }
    }

    static components = { TodoItem }
}
