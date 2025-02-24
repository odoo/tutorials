import { Component,useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "./utils";


export class TodoList extends Component {

    static template = "awesome_owl.todolist";
    static components = {TodoItem};

    setup() {
        this.tempid=0;
        this.todos = useState([]);
        useAutofocus("input")
    }

    addTodo(ev) {
        if( ev.keyCode === 13 && ev.target.value != ""){
            this.todos.push(
                {
                    id:this.tempid++,
                    description: ev.target.value,
                    isCompleted: false
                });
            ev.target.value = "";
        }
    }

    toggleTodo(id) {
        this.todos.forEach(todo => {
            if(todo.id === id) {
                todo.isCompleted =!todo.isCompleted;
            }
        });
    }

    removeTodo(id) {
    const index = this.todos.findIndex((todo) => todo.id === id);
    if (index >= 0) {
      // remove the element at index from list
      this.todos.splice(index, 1);
    }
    }
}
