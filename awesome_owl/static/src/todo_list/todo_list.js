import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = { TodoItem }

    setup() {
        useAutoFocus("todo-input")
        this.state = useState({todos: [
                { id: 2, description: "penser à acheter du lait", isCompleted: false }, 
                { id: 3, description: "penser à acheter des tomates cerises", isCompleted: true }
            ],
            lastId: 3
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.state.todos.push({id: ++this.state.lastId, description: ev.target.value, isCompleted: false});
            ev.target.value = ""
        }
    }
}
