import { Component, useRef, useState, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";
import { TodoModel } from "./todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.model = useState(new TodoModel());
        useAutofocus("todo_input");
    }

    addTodo(ev) {
        if (ev.keyCode !== 13 || ev.target.value == "") {
            return;
        }
        this.model.add(ev.target.value);
        ev.target.value = "";
    }
}
