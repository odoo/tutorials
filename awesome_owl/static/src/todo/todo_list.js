import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"

    static components = { TodoItem };


    setup() {
        this.todos = useState([]);
        this.cpt = 1;
        this.newTaskInputRef = useRef("newTaskInput");

        onMounted(() => {
            this.newTaskInputRef.el.focus();
        })
    }

    addTodo(ev) {
        if (ev.target.value.length > 0 & ev.keyCode === 13) {
            this.todos.push({
                id: this.cpt,
                description: ev.target.value,
                isCompleted: false,
                toggleState: (id) => { this.toggleState(id); },
                removeTodo: (id) => { this.removeTodo(id); }
            });
            ev.target.value = "";
            this.cpt += 1;
        }
    }

    toggleState(todoId) {
        let currentTodo = this.todos.find((todoItem) => todoItem.id == todoId);
        if (currentTodo) {
            currentTodo.isCompleted = !currentTodo.isCompleted;
        }
    }

    removeTodo(todoId) {
        let todoToRemoveIndex = this.todos.findIndex((todoItem) => todoItem.id == todoId);
        if (todoToRemoveIndex >= 0) {
            this.todos.splice(todoToRemoveIndex, 1);
        }
    }

}