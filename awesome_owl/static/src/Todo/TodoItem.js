import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem"
    static props = ['todo', "onChange?", "removeTodo?"]
    setup() {

    }
    checked(event) {
        if (this.props.onChange) {
            console.log(this.props.todo)
            this.props.onChange(event.target.id);
        }
    }
    removeTodo(event) {
        console.log("removed function called")
        console.log(this.props.removeTodo)
        console.log(event.target)
        if (this.props.removeTodo) {
            console.log(event.target.id)
            this.props.removeTodo(event.target.id)
        }
    }
}
