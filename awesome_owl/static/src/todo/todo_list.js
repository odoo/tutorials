// todolist
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { TodoList as TodoListModel } from "./todo_model";

export class TodoListView extends Component {
    static template = "awesome_owl.TodoListView";
    static components = { TodoItem };

    setup() {
        this.model = useState(new TodoListModel());
    }

    addTodoItem() {
        this.model.addTodo("New Todo");
    }

    removeTodoAt(index) {
        this.model.removeTodo(index);
    }

    addTodo(ev) {
        const value = ev.target.value.trim();
        if (ev.key === "Enter" && value) {
            this.model.addTodo(value);
            ev.target.value = "";
        }
    }
}
