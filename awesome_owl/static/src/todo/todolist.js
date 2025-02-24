import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../util";

export class TodoList extends Component {
    static template = "awesome_owl.todo.list";
    
    setup(){
        this.state = useState({
            num: 0,
            todos:[]
        });
        this.todoInputRef = useAutofocus("todoInput");
    }

    addTodo(ev){
        if (ev.keyCode == 13){
            const newTodo = ev.target.value.trim();
            if(newTodo){
                this.state.num++;
                this.state.todos.push({
                    id: this.state.num,
                    description: newTodo,
                    isCompleted: false
                })
            }
            ev.target.value = "";
        }
    }

    removeTodo(id) {
        this.state.todos = this.state.todos.filter(todo => todo.id !== id);
    }

    static components = {TodoItem};
}
