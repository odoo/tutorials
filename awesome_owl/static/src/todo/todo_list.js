import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Todo } from "./todo";
import { Card } from "../card/card";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { Card, TodoItem };

    ids = 0
    
    setup() {
        this.state = useState({ todos: [], input: ''})
    }

    keyup(event) {
        if(event.keyCode === 13) {
            this.state.todos.push(new Todo(this.ids++, event.srcElement.value, false))
        }
    }
}

