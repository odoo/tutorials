import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo.item";

    static props = {
        id : { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        removeTodo: { type: Function },
    }

    setup(){
        this.state = useState({
            id : this.props.id,
            description : this.props.description,
            isCompleted : this.props.isCompleted,
        });
    }

    toggleState(){
        this.state.isCompleted = !this.state.isCompleted;
    }

    removeMe(){
        this.props.removeTodo(this.state.id);
    }
}