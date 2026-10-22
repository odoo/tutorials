import {TodoItem} from "./TodoItem"
import {Component, onMounted, useRef, useState} from "@odoo/owl";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem}

    setup() {
        this.todos = useState([])
        this.myRef = useRef('input')
        onMounted(() => {
            this.myRef.el?.focus()
        })
    }

    addTodo(e) {
        if (e.keyCode === 13) {
            if (e.target.value) {

                this.todos.push({
                    id: this.todos.length + 1, description: e.target.value.trim(), isCompleted: false
                })
                e.target.value = ''
            }
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(((todo) => todo.id === todoId))
        if (index >= 0) this.todos.splice(index, 1);
    }
}
