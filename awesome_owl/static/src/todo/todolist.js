import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }
    static props = {}

    setup() {
        this.nextId = 1;
        this.state = useState({
            newTodoName: "",
            todos: []
        });
        this.myRef = useRef('inputTodo');
        onMounted(() => {
            this.myRef.el.focus();
        });
    }

    toggleTodo(todoId) {
        const todo = this.state.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = this.state.newTodoName.trim();
            if (description) {
                this.state.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });

                this.state.newTodoName = "";
            }
        }
    }

    removeTodo(todoId) {
        const index = this.state.todos.findIndex((elem) => elem.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }

}
