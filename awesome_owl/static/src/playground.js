/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static props = {};

    static template = "awesome_owl.playground";
    static components = { Card, TodoList };

    setup() {
        this.link = markup(`<a href='https://pierre.barracudapps.com'>Pierre LAMOTTE</a>`);
    }
}
