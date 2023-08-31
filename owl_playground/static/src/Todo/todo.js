/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Todo extends Component {
  static template = "owl_playground.Todo";
  static props = {
    todo: {
      id: { type: Number },
      description: { type: String },
      done: { type: Boolean },
    },
    toggleTodo:{type:Function}

  };
  onClick(ev){
    this.props.toggleTodo(this.props.todo.id)
  }
}
