import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    setup() {
        this.state = useState({todos: []});
        this.counter = 0;
        this.inputTodo = useRef("inputTodo");

        onMounted(() => {
            this.inputTodo.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value != "") {
            this.state.todos.push({
                id: this.counter++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodoState = (todoId) => {
        const todo = this.state.todos.find((t) => t.id === todoId);
        if (todo) {
            if (todo.isCompleted) {
                todo.isCompleted = false;
            } else {
                todo.isCompleted = true;
            }
        }
    }

    removeTodo = (todoId) => {
        const index = this.state.todos.findIndex((t) => t.id === todoId);
        this.state.todos.splice(index, 1);
    }

    static components = { TodoItem };
}
