import { Component } from "@odoo/owl"


export class TodoItem extends Component {
    static template = "awesome_owl.todo.item"
    static props = ['todo', 'toggleState', 'deleteTodo']
}
