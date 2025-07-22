import { Component, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/components/todo_list/todo_item";
import { useAutoFocus } from "@awesome_owl/lib/utils";

export class TodoList extends Component {
    static template = "awsome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.state = useState({ nextId: 1, todos: [] })
        this.inputRef = useAutoFocus("add-input");
    }

    addTodo(e) {
        if (e.keyCode === 13) {
            const todoDesc = e.target.value.trim();
            e.target.value = "";
            if (todoDesc) {
                const newTodo = {
                    id: this.state.nextId++,
                    description: todoDesc,
                    isCompleted: false
                }
                this.state.todos.push(newTodo);
            }
        }
    }

    deleteTodo(id) {
        const index = this.state.todos.findIndex(t => t.id == id)
        if (index >= 0) {
            this.state.todos.splice(index, 1)
        }
    }


    toggleTodoState(id) {
        const todo = this.state.todos.find(t => t.id == id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

}
