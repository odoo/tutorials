import { Component, useState, onMounted, useRef} from "@odoo/owl"
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = { TodoItem };

    setup() {
        // in TodoList
        this.todos = useState([
            // { id: 2, description: "write tutorial", isCompleted: true },
            // { id: 3, description: "buy milk", isCompleted: false },
        ]);
        this.nextId = 1;

        this.inputRef = useRef("todo-input");

        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    addTodo(ev) {
        if (ev.keyCode == 13) {
            const description = ev.target.value.trim();

            if (description !== "") {
                this.todos.push({
                    id:this.nextId++,
                    description: description,
                    isCompleted: false,
                });

                ev.target.value = "";
            }
        }
    }
}