/** @odoo-module **/

const { Component } = owl;

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        onChange: {
            type: "Function"
        },
        onDelete: {
            type: "Function"
        }
    }

    checkBoxClicked() {
        this.props.onChange(this.props.todo.id);
    }

    deleteClicked() {
        this.props.onDelete(this.props.todo.id);
    }


}
