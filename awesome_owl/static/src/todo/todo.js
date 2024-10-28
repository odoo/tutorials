import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";

export class TodoItem extends Component {
    static template = "awesome_owl.todo.item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            },
        },
        toggle_callback: { type: Function },
        remove_callback: { type: Function },
    };

    setup() {
        this.onChange = this.onChange.bind(this);
        this.onClick = this.onClick.bind(this);
    }

    onChange() {
        this.props.toggle_callback(this.props.todo.id);
    }

    onClick() {
        this.props.remove_callback(this.props.todo.id);
    }
}

export class TodoList extends Component {
    static template = "awesome_owl.todo.list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.addToDo = this.addToDo.bind(this);
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);

        useAutofocus("input");
    }

    addToDo(event) {
        let name = event.target.value;
        if (event.keyCode === 13 && name.length) {
            this.todos.push({
                id: this.todos.length + 1,
                description: name,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    toggleState(id) {
        this.todos[id - 1].isCompleted = !this.todos[id - 1].isCompleted;
    }
}
