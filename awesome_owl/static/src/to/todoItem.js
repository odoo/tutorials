import {Component} from '@odoo/owl'

export class TodoItem extends Component{
    static template = "awesome_owl.TodoItem";
    static props = {
        todo:{type: Object, optional: false},
        toggleState:{type: Function, optional: true},
        removeTodo:{type: Function, optional: true},
    };
    change(ev) {
        if(this.props.toggleState){
            this.props.toggleState(this.props.todo);
        }
    }
    cancelClick() {
        if(this.props.removeTodo){
            this.props.removeTodo(this.props.todo.id);
        }
    }
}
