/** @odoo-module **/

import { Component , useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    
    setup() {
        this.todos = useState([]);
        this.cur_id=0;
    }

    addTodo(ev) {
        if  (ev.keyCode === 13 && ev.target.value != ""){
            this.cur_id++;
            this.todos.push({
                id:this.cur_id,
                description:ev.target.value,
                isCompleted:false
            });
            ev.target.value = "";
        }

    }

}
