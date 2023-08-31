/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Todo } from "./Todo/todo";

export class Playground extends Component {
  static template = "owl_playground.playground";
  static components = { Counter,Todo };
  setup(){
    this.todo = {id:3,description:"buy milk",done:true}
  }
}
