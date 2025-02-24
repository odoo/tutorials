import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todolist"
    setup() {
        this.todos = useState([{ id: 0, description: "buy milk", isCompleted: false }, { id: 1, description: "buy eggs", isCompleted: true }]);
        useAutofocus("addTodoRef");
    }
    addTodo(ev) {
        //ev.target
        if (ev.key === "Enter" && ev.target.value.length > 0) {
            this.todos.push({ id: this.todos.length, description: ev.target.value, isCompleted: false })
        }
    }
    toggleState(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos[index].isCompleted = !this.todos[index].isCompleted;
        }
    }
    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
    static components = { TodoItem };

}
