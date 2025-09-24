import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Todo } from "./todo";
import { Card } from "../card/card";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { Card, TodoItem };

    setup() {
        this.ids = 0;
        this.state = useState({ todo_list: [], input: "" });
        useAutofocus("todo_input");
    }

    keyup(event) {
        if (event.keyCode === 13) {
            this.state.todo_list.push(
                new Todo(this.ids++, event.target.value, false),
            );
        }
    }

    remove(id) {
        const index = this.state.todo_list.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.state.todo_list.splice(index, 1);
        }
    }
}
