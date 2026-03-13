import { Component,useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";
export class TodoList extends Component {
    
    static template = "awesome_owl.TodoList";
    static components = { TodoItem};
    
    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("input");
}

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();

            if (!description) {
                return;
            }

            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });

            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
    
    const index = this.todos.findIndex((todo) => todo.id === todoId);
    if (index >= 0) {
        this.todos.splice(index, 1);
        }
    }
}
