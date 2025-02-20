/** @odoo-module **/

import { Component,markup,useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  setup(){
    this.totalCount = useState({value:0});
  }

  onChange(){
    this.totalCount.value++;
  }

  html1 = markup("<p style='color:red;'>This is some html content</p>");
  html2 = "<p style='color:red;'>This is some html content</p>"

  static components = { Counter, Card, TodoList };
}
