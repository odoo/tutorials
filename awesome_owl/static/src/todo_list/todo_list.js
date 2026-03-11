import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {

    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {

        this.todos = useState([]);

        this.nextId = 1;

        this.inputRef = useRef("input");

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {

        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();
            if (!description) {
                return;
            }
            const newTodo = {
                id: this.nextId++,
                description,
                isCompleted: false
            };

            this.todos.push(newTodo);

            ev.target.value = "";
        }
    }
    toggleState(todoId) {

        const todo = this.todos.find(t => t.id === todoId);

        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId) {

        const index = this.todos.findIndex(
            (todo) => todo.id === todoId
        );

        if (index >= 0) {
            this.todos.splice(index, 1);
        }

    }
}
