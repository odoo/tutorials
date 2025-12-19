import { useState, Component } from "@odoo/owl";
import { TodoItem } from "./todo-item";

export class TodoList extends Component {
    static template = "awesome_owl.todo-list";
    static components = { TodoItem }

    setup() {
        this.state = useState({todos: [], nextId: 1});
    }

    input_event_handler(event) {
        // keyCode is deprecated, use key instead
        if (event.key === "Enter") {
            if (event.target.value) {
                this.state.todos.push({id: this.state.nextId, description: event.target.value, isCompleted: false});
                this.state.nextId++;
                event.target.value = "";
            }
        }
    }
}
