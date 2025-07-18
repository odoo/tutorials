import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todoitem";
  static props = {
    todo: Object,
    toggleState: Function,
    removeTodo: Function,
  };
  onToggle(ev) {
    this.props.toggleState(this.props.todo.id);
  }
  onRemove() {
    this.props.removeTodo(this.props.todo.id);
  }
}
