import { Component, useState, } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "@web/core/utils/hooks";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.nextId=1;
        this.todos = useState([]);
        this.inputRef = useAutofocus({refName:"inputRef"})
    };

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value != ""){
            this.todos.push({
                id: this.nextId++,
                description : ev.target.value,
                isCompleted : false
            })
            ev.target.value="";
        }
    };

    toggleTodo(todoId){
        const todo = this.todos.find((todo) => todo.id === todoId);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    };
    
    removeTodo(remId) {
        this.todos.splice(0, this.todos.length, ...this.todos.filter(el => el.id !== remId));
    }
}
