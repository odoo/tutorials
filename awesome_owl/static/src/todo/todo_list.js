import { Component, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup(){
        this.inputRef = useAutofocus("InputValue")
        this.todos = useState([]);
        this.nextId = 1
        this.inputValue = useState({ text: "" });
        this.removeTodo = this.removeTodo.bind(this);
    }

    addTodo(ev)
    {
        if (ev.keyCode != 13) return
        this.todos.push({
            id : this.nextId++,
            description : this.inputValue.text,
            isCompleted : false
        })
        this.inputValue.text = ""
    }

    toggleTodo = (id) => {
        const todo = this.todos.find(t => t.id == id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
