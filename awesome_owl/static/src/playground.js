/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
      this.totalCount = useState({value:0});
      this.html1 = markup("<p style='color:red;'>This is some html content</p>");
      this.html2 = "<p style='color:red;'>This is some html content</p>"
    }

    onChange() {
      this.totalCount.value++;
    }

    static components = { Counter, Card, TodoList };
}
