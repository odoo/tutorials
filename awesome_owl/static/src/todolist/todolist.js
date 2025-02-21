import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list_template";
    static components = { TodoItem };
    static props={}

    setup() {
        this.todos = useState([]);
        this.todocounter = 1;
        this.inputref = useAutofocus();
        this.todos1 = [{id:1,description:"Buy cat",isCompleted:false},{id:2,description:"Buy krishna",isCompleted:false}]
    }

    addtodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim()

            if (description) {
                this.todos.push({ id: this.todocounter++, description, isCompleted: false });
                input.value = "";
            }
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(todo => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

}
