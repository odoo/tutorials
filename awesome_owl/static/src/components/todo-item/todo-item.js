import {Component} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleState: Function,
        removeTodo: Function,
    }

    setup() {
        super.setup();
    }

    toggleState(ev) {
        // You can use !this.state.isCompleted instead of ev.target.checked if you want
        // to just toggle the state without getting the state from the DOM
        this.props.toggleState(this.props.id, ev.target.checked);
    }

    removeTodo(e) {
        e.preventDefault();
        e.stopPropagation();

        if (confirm(_t("Do you confirm the removal of this todo ?"))) {
            this.props.removeTodo(this.props.id);
        }
    }
}
