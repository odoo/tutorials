import { Component,useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";


export class TodoList extends Component {

    static template = "awesome_owl.todolist";
    static components = {TodoItem};

    setup() {

        this.tempid=0;
        this.todos = useState([]);
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
}
