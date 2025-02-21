import {Component} from "@odoo/owl";

export class TodoItem extends Component{
    static props={
        todo:{id: Number, description: String, isCompleted: Boolean}
    };
    setup() {
        console.log("TodoItem received todo:", this.props.todo);
    }
    static template = "awesome_owl.todo_item";
}