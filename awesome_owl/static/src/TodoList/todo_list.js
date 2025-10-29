import { Component ,useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static props = {};
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;

        // hook will automatically focus the input on mount
        this.inputRef = useAutoFocus("taskInput");
    }

    addTodo(ev) {
         // Check if Enter was pressed
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value.trim(),
                isCompleted: false,
            });
            // Clear input
            ev.target.value = "";
        }
    }
    
    toggleState(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }
}    