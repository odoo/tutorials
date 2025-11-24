import { Component, useState } from "@odoo/owl";
import TodoItem from "./todo_item";
import { useAutofocus } from "../utils";

class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = { TodoItem };
    static props = {}

    setup() {
        this.state = useState({ todos: [], counter: 0 });
        this.inputRef = useAutofocus({ refName: "input" });
    }

    addTodo(event) {
        if (event.keyCode === 13) {
            const value = event.target.value;
            if (value.length) {
                this.state.counter++;
                this.state.todos = [
                  ...this.state.todos,
                  {
                      id: this.state.counter,
                      description: event.target.value,
                      isCompleted: false,
                  },
                ];
                event.target.value = "";
            }
        }
    }
}

export default TodoList;
