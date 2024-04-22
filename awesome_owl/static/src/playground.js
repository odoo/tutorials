/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card"
import { TodoList } from "./todo_list/todo_list"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }

    setup(){
        this.html = "<div> This is a dev </div>";
        this.html_markup = markup(this.html);
        this.state = useState({sum:0})
    }

    incrementSum(){
        this.state.sum++
    }


}
