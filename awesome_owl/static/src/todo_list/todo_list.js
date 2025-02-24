import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { TodoModel } from "./todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    inputRef = useRef('todoInput');

    setup() {
        this.model = useState(new TodoModel());
        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.model.add(ev.target.value);
            ev.target.value = "";
        }
    }
    static components = { TodoItem };
}
