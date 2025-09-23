// todolist
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { TodoModel } from "./todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.model = useState(new TodoModel());
    }

    addTodoItem() {
        this.model.addTodo("New Todo");
    }

    addTodo(ev) {
        const value = ev.target.value.trim();
        if (ev.key === "Enter" && value) {
            this.model.addTodo(value);
            ev.target.value = "";
        }
    }
}
