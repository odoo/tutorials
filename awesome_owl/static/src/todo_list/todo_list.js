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

    toggleState(id){
        let todo = this.todos.filter((todo) => todo.id == id)
        todo[0].isCompleted = !todo[0].isCompleted
    }

    deleteTodo(id){
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) this.todos.splice(index, 1);
    }
}
