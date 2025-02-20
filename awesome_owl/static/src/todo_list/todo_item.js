import { Component ,useState} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static components = {};
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
        removeTodo: Function,
    };

    setup() {
        this.state = useState({todo: this.props.todo});
    }

    toggleTodo(){
        this.props.toggleState(this.state.todo);
    }
}
