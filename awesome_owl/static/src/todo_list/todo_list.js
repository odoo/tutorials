import { Component, onMounted, useRef, useEffect, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";


export class TodoList extends Component {
    static template = "todo_list.todo_list";
    static components = { TodoItem };

    index = 0
    todo_records = []

    todos = useState(this.todo_records);

    setup(){
        this.useAutofocus("todo_item_input");
    }

     useAutofocus(name) {
        let ref = useRef(name);
        useEffect(
            (el) => el && el.focus(),
            () => [ref.el]
        );
    }

    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value) {
            this.index += 1;
            this.todos.push({"id": this.index, "description": ev.target.value, is_completed: false})
            ev.target.value = "";
        }
    }

    toggleState(ev, el){
        el.is_completed = ev.target.checked;
    }


    removeTodo(todo){
        const index = this.todos.findIndex((elem) => elem.id === todo.id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}