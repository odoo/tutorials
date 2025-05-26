import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Todo, TodoModel } from "./todo";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {
        TodoItem
    }

    setup(){
        this.todoModel = useState(new TodoModel());
        this.inputRef = useRef('input');
        onMounted(()=>this.inputRef.el.focus());
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value != "")
        {
            this.todoModel.add(ev.target.value);
            ev.target.value = "";
        }
    }
}