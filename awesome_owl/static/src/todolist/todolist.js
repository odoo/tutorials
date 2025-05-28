
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "./utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    
    setup() {
        this.todos = useState([]);
        
        useAutofocus("myInput");
    }
    
    addTodo(ev) {
        if (ev.keyCode === 13) {
            var todoId;
            if (this.todos.length == 0) {
                todoId = 1;
            } else {
                todoId = this.todos[this.todos.length -1].id + 1;
            }
            var content = document.querySelector(".todo_content");
            if (content.value != "") {
                this.todos.push({ id: todoId, description: content.value, isCompleted: false });
                content.value = "";
            }
        }
    }
}
