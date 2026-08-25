import { Component, useState, useRef, onMounted } from "@odoo/owl";

import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.inputAutofocusRef = useAutoFocus("input")

        this.toggleState = this.toggleState.bind(this)
    }

    addTodo(event) {
        if (event.keyCode === 13) {
            const lastElement = this.todos.slice(-1)?.[0]
            const lastId = lastElement?.id ?? 0
            this.todos.push({ id: lastId + 1, description: event.target.value, isCompleted: false });
            event.target.value = ""
        }
    }

    toggleState(refId) {
        const element = this.todos.find(({id}) => id === refId);
        if (element) element.isCompleted = !element.isCompleted;
    }
}
