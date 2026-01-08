import { Component } from '@odoo/owl';

class TodoItem extends Component {
    static props = {
        todo: Object,
        toggleState: Function,
        removeTodo: Function,
    };

    toggleTodo() {
        this.props.toggleState(this.props.todo.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

