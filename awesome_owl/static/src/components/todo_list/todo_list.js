import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup () {
        this.todos = useState([]);
        this.ids = useState({"last_id": 0});
        useAutoFocus("input");
    }

    addTodo (ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.ids.last_id += 1
            this.todos.push({
                id: this.ids.last_id,
                title: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todo_id) {
        const index = this.todos.findIndex(t => t.id === todo_id);
        if (index !== -1) {
            this.todos[index].isCompleted = !this.todos[index].isCompleted;
        }
    }

    deleteTodo(todo_id){
        const index = this.todos.findIndex(t => t.id === todo_id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }

}
