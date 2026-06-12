import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: {
            type: Object,
            optional: false,
        },
        toggleState: {
            type: Function,
            optional: true,
        },
        handleDelete: {
            type: Function,
            optional: true,
        }
    };

    handletoggleState() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id);  // pass id up
        }
    }

    handleDelete() {
        if (this.props.handleDelete) {
            this.props.handleDelete(this.props.todo.id);  // pass id up
        }
    }

}
