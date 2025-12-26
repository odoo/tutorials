import { markup, Component, useState, useRef, onMounted, reactive } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todoList/todoList";
import { useAutoFocus } from "./utils";
import { TodoModel } from "./todo/todoModel";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};


    setup() {
        this.todoInput = useRef("todoInputRef");
        this.state = useState({ model: new TodoModel(), isOpened: true });
        useAutoFocus({ refName: "todoInputRef" })
    }
    updateSum() {
        this.state.sum++;
    }
    addTodo(ev) {
        if (ev.keyCode === 13 && this.todoInput.el.value != "") {
            this.state.model.addTodo(this.todoInput.el.value)
            this.todoInput.el.value = "";
        }
    }
    toggleIsOpened() {
        this.state.isOpened = !this.state.isOpened;
    }
}
