/** @odoo-module **/

import { Component, useState ,useRef, onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        // this.todos = useState([
        //     { id: 1, description: "Buy milk", isCompleted: false},
        //     { id: 2, description: "Read a book",isCompleted: true},  // here is no value or missing isCompleted, means that isCompleted is not present here == undefined, in the js undefined treated as false (Falsy)
        //     { id: 3, description: "Walk the dog", isCompleted: true },
        // ]);  //hard coded

        this.todos = useState([]);
        this.nextId = 1;

        this.inputRef=useAutofocus("inputRef");
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value.trim() !== "" ) {
            const newTodo = {
                id: this.nextId++, 
                description: event.target.value.trim(),
                isCompleted: false,
            };
            this.todos.push(newTodo);
            event.target.value = "";  
            console.log(this.todos)
            // doubt// onmounted or setup !!
        }
    }

    toggleState(todoId) {
        // debugger
        console.log(this.todos)
        console.log()
        // this.todos = this.todos.map(todo =>
        //     todo.id === todoId ? { ...todo, isCompleted: !todo.isCompleted } : todo
        // );
        const todo=this.todos.find((todo)=>todo.id===todoId);
        if(todo){
            todo.isCompleted=!todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(todo => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1); 
        }
    }
}
