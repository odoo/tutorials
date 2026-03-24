import {Component, useState} from "@odoo/owl";
import {TodoItem} from "../todo-item/todo-item";
import {useAutoFocus} from "../../utils";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {
        TodoItem,
    }

    static props = {
        description: {type: String, optional: true},
    }

    setup() {
        super.setup();

        this.notification = useService("notification");

        useAutoFocus("todoInput");

        this.state = useState({
            todos: this._getTodos(),
        });
    }

    todoOnKeyup(event) {
        if (event.keyCode !== 13) {
            return;
        }

        const value = event.target.value;

        if (!value || value.trim() === "") {
            return;
        }

        const max = (this.state.todos.length ? Math.max(...this.state.todos.map(todo => todo.id)) : 0) + 1;

        this._addTodo({id: max, description: value, isCompleted: false});

        event.target.value = "";

        this.notification.add(_t("Todo added successfully!"), {type: "success"});
    }

    _getTodos() {
        const todos = localStorage.getItem("todos");

        if (!todos) {
            return [];
        }

        try {
            return JSON.parse(todos);
        } catch (_error) {
            return [];
        }
    }

    _saveTodos() {
        localStorage.setItem("todos", JSON.stringify(this.state.todos));
    }

    _addTodo(todo) {
        this.state.todos.push(todo);

        const todos = this._getTodos();

        todos.push(todo);

        this._saveTodos();
    }

    toggleItemState(id, state) {
        this.state.todos.find(x => x.id === id).isCompleted = state;
    }

    removeTodo(id) {
        const index = this.state.todos.findIndex(x => x.id === id);

        if (index !== -1) {
            this.state.todos.splice(index, 1);

            this._saveTodos();
        }
    }
}
