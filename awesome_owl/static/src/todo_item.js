import { Component, xml } from "@odoo/owl";


export class TodoItem extends Component {
    static props = ['todo', 'toggleState', 'removeTodo']
    static template = "awesome_owl.todo_item"
}
