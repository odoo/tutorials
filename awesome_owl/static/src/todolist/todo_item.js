import { Component } from '@odoo/owl';

export class TodoItem extends Component {
    static template = 'awesome_owl.TodoItem';
    static props = ['todo', 'deleteTodo']; 
    setup(){this.upperCaseOne = this.upperCaseOne.bind(this) }
    onChange(){this.props.todo.isCompleted = !this.props.todo.isCompleted}
    upperCaseOne() {this.props.todo.description = this.props.todo.description.toUpperCase()}
}
