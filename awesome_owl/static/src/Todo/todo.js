import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";


export class TodoItem extends Component {
    static template = "awesome_owl.todoItem"
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        onToggleComplete: Function,
        onClickDelete: Function
    }
    toggleState() {
        this.props.onToggleComplete(this.props.todo.id)
    }
    removeTask() {
        this.props.onClickDelete(this.props.todo.id)
    }
}
export class TodoList extends Component {
    static template = "awesome_owl.todoList"
    setup() {

        this.state = useState({
            newTask: "",
            todo: [
                { id: 1, description: "Buy milk", isCompleted: false },
                { id: 2, description: "Go to gym", isCompleted: true }
            ]
        });
        this.inputRef = useAutofocus();
    }

    checkEnter(ev) {
        if (ev.keyCode === 13) { this.addTodo() }
    }

    addTodo() {
        if (this.state.newTask.trim().length == 0) return
        const newId = this.state.todo.length + 1
        this.state.todo.push({ id: newId, description: this.state.newTask.trim(), isCompleted: false })
        this.state.newTask = ""

    }
    static components = { TodoItem }
    onToggleComplete(tid) {
        const updatedTodos = this.state.todo.map(t =>
            t.id === tid ? { ...t, isCompleted: !t.isCompleted } : t
        );
        this.state.todo = updatedTodos;
    }
    onClickDelete(tid) {
        const updatedTodos = this.state.todo.filter(t => t.id !== tid)
        this.state.todo = updatedTodos
    }

}
