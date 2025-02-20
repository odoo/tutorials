import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";

  static props = {
    todo_item: { type: Object },
    callbackToggleState: { type: Function },
    callbackRemoveTodo: { type: Function },
  };

  removeTodo = (removeTodoId) => {
    this.props.callbackRemoveTodo(removeTodoId);
  };

  toggleState = (todoId) => {
    this.props.callbackToggleState(todoId);
  };
}
