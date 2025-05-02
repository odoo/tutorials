import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "./utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [],
            idCounter: 0
        });
        useAutofocus("input_todo");
    };

    addTodo(ev) {
        if (ev.keyCode === 13) {
            this.state.idCounter++
            this.state.todos.push({
                'id': this.state.idCounter, 'description': ev.target.value, 'isCompleted': false
            });
            ev.target.value = "";
        }
    };

    toggleState(todoId) {
        let todo = this.state.todos.find(todo => todo.id === todoId);
        todo.isCompleted = !todo.isCompleted;
    }
}
