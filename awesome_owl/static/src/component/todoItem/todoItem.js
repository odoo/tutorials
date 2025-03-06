/** @odoo-module **/

const { Component } = owl;

export class TodoItem extends Component {
    static template = "awesome_owl.todoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        toggleState: Function,
        removeTodo: Function
    }

    toggleState = () => {
        this.props.toggleState(this.props.todo);
    }

    removeTodo = () => {
        this.props.removeTodo(this.props.todo);
    }
}
