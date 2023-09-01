/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Todo extends Component {
  static template = "owl_playground.Todo";
  static props = {
    todo: {
      type:Object,
      id: { type: Number },
      description: { type: String },
      done: { type: Boolean },
    },
    toggleTodo:{type:Function},
    removeTodo:{type:Function}

  };
  onClick(ev){
    this.props.toggleTodo(this.props.todo.id)
  }
  onRemove(ev){
    this.props.removeTodo(this.props.todo.id);
  }
}
