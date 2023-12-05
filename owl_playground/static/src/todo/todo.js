/** @odoo-module **/

import { useState, useRef, Component } from "@odoo/owl"
import { useAutoFocus } from "../utils/utils";

export class Todo extends Component {
    static template = "todo.todo";

    static props = {
        id: Number,
        description: String,
        done: Boolean,
        toggleState: Function,
        removeFromList: Function
    }

    onCheckboxClick() {
        this.props.toggleState(this.props.id);
    }

    onRemoveClick() {
        this.props.removeFromList(this.props.id);
    }
}

export class TodoList extends Component {
    static template = "todo.todolist";
    static components = { Todo };

    setup() {
        useAutoFocus(useRef("todoInput"));
        this.todos = useState(
            [
                { id: 1, description: "buy milk", done: false },
                { id: 2, description: "buy eggs", done: false },
                { id: 3, description: "buy avocado", done: false },
            ]
        );
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value) {
            let util = this.findTodoID(this.todos);
            this.todos.splice(
                util.index,
                0,
                {
                    id: util.id,
                    description: e.target.value,
                    done: false
                }
            );
            e.target.value = "";
        }
    }

    findTodoID(todos) {

        let idExists = true;
        let util = { index: 0, id: 0 };
        let i = 0;

        while (idExists) {

            ++util.id;
            i = 0;

            while (i < todos.length && !(idExists = (util.id === todos[i].id)))
                ++i;

            if (idExists)
                util.index = i + 1;

        }

        return util;

    }

    toggleTodo(id) {
        const todo = this.todos.find((todo) => { return todo.id === id; });
        if (todo) {
            todo.done = !todo.done;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => { return todo.id === id; });
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
