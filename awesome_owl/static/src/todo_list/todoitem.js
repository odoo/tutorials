import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todoitem";
  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
    },
    toggleTodoStatus: Function,
    removeTodo: Function,
  };

  todoHandler(){
    this.props.toggleTodoStatus(this.props.todo.id);
  }

  deleteTodo(){
    this.props.removeTodo(this.props.todo.id);
  }

}
