import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = { 
        TodoItem,
    }

    static props = {
    }

    setup() {
        this.state = useState({
            text: "",
            todos: [],
            
        })
        this.last_id = 0
        this.inputRef = useRef('input')

        onMounted(() => {
            this.inputRef.el.focus()
        });

        this.toggleState = this.toggleState.bind(this)
        this.removeTodo = this.removeTodo.bind(this)
    }

    toggleState(id) {
        const index = this.state.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.state.todos[index].isCompleted = !this.state.todos[index].isCompleted
        }
    }

    removeTodo(id) {
        const index = this.state.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.state.todos.splice(index, 1)
        }
        
    }

    addTodo(event) {
        if (this.state.text == "") return
        if (event.keyCode == 13) {
            const newTodo = { id: this.last_id, description: this.state.text, isCompleted: false }
            this.state.todos.push(newTodo)
            this.last_id = this.last_id + 1
        }
    }
}
