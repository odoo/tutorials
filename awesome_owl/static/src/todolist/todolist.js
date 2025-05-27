
import { Component, useState, xml } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    
    setup() {
        this.todos = useState([]);
    }
    
    addTodo(ev) {
        if (ev.keyCode === 13) {

            console.debug(this.todos);
            console.debug(this.todos.length);
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
