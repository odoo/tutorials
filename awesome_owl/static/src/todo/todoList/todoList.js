/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoItem/todoItem";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup(){
        this.todos = useState([
            { id: 1, description: "Faire les courses", flag: false },
            { id: 2, description: "Répondre aux e-mails", flag: true },
            { id: 3, description: "Préparer la réunion", flag: false }
        ]);
    }
}