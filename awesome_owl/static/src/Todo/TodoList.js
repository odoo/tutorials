import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./TodoItem";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    unique_id = 0
    setup() {
        this.state = useState([]);
        this.inputRef = useRef("input");
        this.removeTodo = this.removeTodo.bind(this)
        onMounted(() => {
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
            else {
                console.log("No Element found!!")
            }
        });
    }
    static components = { TodoItem }
    addTodo(event) {
        if (event.keyCode === 13) {
            this.state.push({ id: this.unique_id, description: event.target.value, isCompleted: false })
            this.unique_id++
            event.target.value = ""
            console.log("Added vals")

        }

    }
    toggleState(todoId) {
        console.log("This is checked!")
        console.log(todoId)
        const todo = this.state.find(todo => todo.id == todoId);
        console.log(todo)
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }

    }
    removeTodo(todoId) {
        console.log("THIS FUNCTION IS CALLED!!!")
        const todoIndex = this.state.findIndex(todo => todo.id == todoId);
        console.log("Todo index:", todoIndex);  // Log the index to verify

        if (todoIndex !== -1) {
            // Remove the todo from the state array using `splice`
            this.state.splice(todoIndex, 1);
            console.log("Todo removed:", this.state);
        } else {
            console.error("Todo not found with id:", todoId);
        }
    }
}
