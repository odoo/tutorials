/** @odoo-module **/

import { Component , useState ,useRef,onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import {focus_element} from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    
    setup() {
        this.todos = useState([]);
        this.cur_id=0;
        focus_element("input");
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

    toggleTodo(todoId) {
        const todo = this.todos[todoId];
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

}
