import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { Todoitem } from "./todoitem.js";
// import { useAutofocus } from "@/hooks/useAutofocus.js";

export class Todolist extends Component {
    static template = "my_module.Todolist";
    static components = { Todoitem };

    setup() {
        this.myRef = useRef("todoInput");
        onMounted(() => {
            this.myRef.el.focus();
        });
        this.todos = useState({
            items: [],
        });
    }
    addTodo(ev) {
        this.myRef.el.focus();
        if(ev.keyCode===13 && ev.target.value.trim()!==""){
            const newId = this.todos.items.length
                ? this.todos.items[this.todos.items.length - 1].id + 1
                : 1;
            this.todos.items.push({ id: newId, description: ev.target.value.trim(), isCompleted: false });
            ev.target.value = "";
        }
    }
    toggleState(id, isCompleted) {
        const todo = this.todos.items.find((item) => item.id === id);
        if (todo) {
            todo.isCompleted = isCompleted;
        }
    }
    onRemove(id) {
        console.log("Todolist onRemove", id);
        this.todos.items = this.todos.items.filter((item) => item.id !== id);
    }
}
