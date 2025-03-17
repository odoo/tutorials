import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    static props = {};


    setup() {
        this.todos = useState([]);
        this.idCounter = 0;
        this.elementRef = useAutoFocus("input_focus");
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();

            if (description) {
                this.todos.push({
                    id: ++this.idCounter,
                    description: description,
                    isCompleted: false,
                });
            }
            input.value = "";
        }
    }

    toggleState(id){
        const todo = this.todos.find((todo) => todo.id === id);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id){
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

}
