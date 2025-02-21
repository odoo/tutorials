/** @odoo-module**/

import { onMounted, useRef, useState, Component } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.state = useState({newTodo: ""});
        //this.inputRef = useRef("new_todo");
        useAutoFocus("new_todo");
        /*onMounted(() => {
            this.inputRef.el.focus();
        });*/
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && this.state.newTodo){
            this.todos.push({
                id: (this.todos.length > 0 ? ((Math.max(...this.todos.map(t => t.id))) + 1) : 0),
                description: this.state.newTodo,
                isCompleted: false
            });
            this.state.newTodo = "";
        }
    }

}
