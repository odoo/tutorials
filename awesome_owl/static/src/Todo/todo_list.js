/** @odoo-module **/

import { Component, useState ,useRef, onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "@web/core/utils/hooks";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static props={};

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef=useAutofocus({refName: "inputRef"});
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
        }
    }

    toggleState(todoId) {
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
    
    // removeTodo(todoId) {
    //     const updatedList = this.todos.filter(todo => todo.id !== todoId);
    //     this.todos = updatedList;
    // }
}
