import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todo_item"
import { useAutofocus } from "../utils"


var id = 1

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    
    static components = { TodoItem }
    
    setup() {
        this.state = useState([])
        useAutofocus('input')
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            this.state.push({id: id, description: ev.target.value.trim(), isCompleted: false})
            id++
            ev.target.value = ""
        }
    }

    removeTodo(id) {
        const index = this.state.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.state.splice(index, 1);
        }
    }
}
