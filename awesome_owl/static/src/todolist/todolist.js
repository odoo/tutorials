import { Component, useState } from "@odoo/owl";
import { ToDoItem }  from "./todoitem";
import { useAutofocus } from "../util.js";
import { ToDoModel } from "./todomodel";

export class ToDoList extends Component {
    static template = "awesome_owl.ToDoList";
    static components = { ToDoItem };

    setup() {
        this.model = useState(new ToDoModel())
        useAutofocus("inputAddTodo");
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value != ''){
            this.model.add(ev.target.value);
            ev.target.value = "";
        }
    }
}   
