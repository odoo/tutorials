/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

import {Card} from "../card/card"
import {TodoItem} from "./todo_item/todo_item";
import {useAutofocus} from "../../util"

export class TodoList extends Component {

    static components = {Card, TodoItem};
    static template = "awesome_owl.todo_list";

    addInput = useState({text: ''})
    todos = useState({})
    nextId = Math.max(Math.max(...Object.keys(this.todos)), 0)

    setup() {
        useAutofocus('add_input')
    }

    // EVENTS

    onKeyUpInput(event) {
        if (event.keyCode === 13) {
            this.onClickAdd()
        }
    }

    onClickAdd() {
        if (this.addInput.text === '')
            return

        let id = this.nextId++;
        this.todos[id] = {id: id, description: this.addInput.text, isCompleted: false}
        this.addInput.text = ''
    }

    // METHODS

    toggleItem(id) {
        if (this.todos[id]) {
            this.todos[id].isCompleted = !this.todos[id].isCompleted
        }
    }

    deleteItem(id) {
        if (this.todos[id]) {
            delete this.todos[id]
        }
    }
}
