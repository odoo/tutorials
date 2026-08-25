import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./TodoItem";
import { useAutofocus} from "./../utils"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.todos = useState([ ]);
        this.state = useState({
            next_id: 1,
        });
        useAutofocus("input_todo");

    }

    onInputKeyup(ev) {
        if (ev.key === "Enter") {
            const value = ev.target.value.trim();
            if (value) {
                const next_id = this.state.next_id++;
                this.todos.push(
                    {
                        id: next_id,
                        description: value,
                        isCompleted: false
                    }
                )
                ev.target.value = "";
            }
        }
    }

    toogleTodoState(id) {
        if (!id) {
            return;
        }
        const todo = this.todos.find(item => item.id === id);

        if (!todo) {
            return;
        }
        todo.isCompleted = !todo.isCompleted
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
               this.todos.splice(index, 1);
        }
    }

}
