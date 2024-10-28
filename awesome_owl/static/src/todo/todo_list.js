/** @odoo-module **/

import { useAutofocus } from "@web/core/utils/hooks";
import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static props = {};

    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.inputRef = useRef("todo_list_add_item");
        useAutofocus({ refName: "todo_list_add_item" });
        this.todos = useState([]);
        this.state = useState({ count: 0 });
    }

    toggleState(id) {
        this.todos[id].isCompleted = !this.todos[id].isCompleted;
    }

    remove(id) {
        debugger
        this.todos = this.todos.filter(function (todo) {
            return todo.id != id;
        })
        this.state.count--;
    }

    /**
     * @param {KeyboardEvent} ev
     */
    onKeyUp(ev) {
        if (ev.key === "Enter") {
            let inputVal = this.inputRef.el.value;
            if (inputVal.trim() !== "") {
                let lastId = this.todos.slice(-1)[0] ?? { id: -1 };
                this.todos.push({ id: lastId.id + 1, description: inputVal, isCompleted: false });
                this.state.count++;
                this.inputRef.el.value = "";
            }
        }
    }
}
