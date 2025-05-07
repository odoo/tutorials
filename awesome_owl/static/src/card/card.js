/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "../counter/counter";
import {TodoList} from "../todo/todo_list";
import {TodoItem} from "../todo/todo_item";

export class Card extends Component {

    static components = { Counter };

    static template = "awesome_owl.card"

    static props = {
        card_title: String,
    };

    setup() {
        this.state = useState({ opened: true });
    }

    toggleCard() {
        this.state.opened = !this.state.opened
    }

    html_bloc_1 = "<div><i>un-escaped text</i></div>";
    // Dangerous because the markup will not escape the strings and thus allows injections.
    html_bloc_2 = markup("<div><i>un-escaped text</i></div>");
}
