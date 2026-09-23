import {Component, useState, useRef, xml, onMounted} from "@odoo/owl"
import {TodoItem} from "./TodoItem"
import {useAutoFocus} from "../utils"


export class TodoList extends Component {
    static template = xml`
        <input placeholder="Enter new task" t-on-keyup="inputEntered"
        t-ref="input_ref" />
        <ul>
        <t  t-foreach="todos" t-as="todo" t-key="todo.id">
<!--        <li><t t-esc="todo.id" />.  <t t-esc="todo.description" /></li>-->
        <div><TodoItem todo="todo" toggleState.bind="toggleTodo"
        removeTodo.bind="onRemoveTodo" /></div>
        </t>
        </ul>
    `

    static components = {TodoItem,};

    setup() {
        this.todos = useState([
            {id: 3, description: "buy milk", isCompleted: true},
            {id: 2, description: "reserver stage", isCompleted: false},
            {id: 8, description: "reserver stage", isCompleted: false},
            {id: 7, description: "reserver stage", isCompleted: false},
        ]);
        this.indexes = useState({
            current: 10,
        })
        this.inputRef = useRef('input_ref');
        useAutoFocus(this.inputRef);
    }

    onRemoveTodo(id) {
        const index = this.todos.findIndex((todo) => (todo.id === id));
        if (index > 0) {
            this.todos.splice(index, 1); // remove elem
        }
    }

    toggleTodo(id) {
        console.log(id);
        const todo = this.todos.find((todo) => (todo.id === id))
        todo.isCompleted = !todo.isCompleted

    }


    inputEntered(event) {
        if (event.keyCode === 13) {
            console.log("Received enter");
            const newTodo = event.target.value;
            if (!newTodo) {
                return
            }
            console.log(newTodo);

            this.todos.push({id: this.indexes.current, description: newTodo, isCompleted: false})
            this.indexes.current++
            event.target.value = ''
        }

    }

}