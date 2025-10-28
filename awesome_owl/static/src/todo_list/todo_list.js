import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {
        TodoItem,
    }

    todos = useState([]);
    ids = 1

    setup() {
        this.myRef = useRef('myInput');
        onMounted(() => {
            console.log(this.myRef.el);
            this.myRef.el.focus()
        });
    }

    addTodos(ev) {
        if(ev.keyCode === 13) {
            if(ev.target.value == "") return;
            this.todos.push({
                id: this.ids,
                description: ev.target.value,
                isCompleted: false,
            })
            this.ids++
            ev.target.value = ""
        }
    }
}
