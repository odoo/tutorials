import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    todos = useState([]);

    setup() {
        this.state = useState({ id_counter: 0 });
    }


    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value !== ""){
            this.todos.push({ id: this.state.id_counter, description: ev.target.value, isCompleted: false });
            this.state.id_counter++;
            ev.target.value = "";
        }
    }

}
