import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";
import {useAutofocus} from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};
    static props = {};

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useAutofocus();
    };

    addTodo(ev) {
        if ((ev.keyCode === 13) && (ev.target.value.length > 0)) {
            this.todos.push({id: this.nextId, description: ev.target.value, isCompleted: false});
            this.nextId++;
            ev.target.value = "";
        }
    };

    toggleState(id) {
        let current_todo = this.todos.find(todo => todo.id === id);
        current_todo.isCompleted = !current_todo.isCompleted

    }
}
