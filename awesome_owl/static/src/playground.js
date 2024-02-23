/** @odoo-module **/

import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {ToDoList} from "./todo/to_do_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";


    setup() {
        this.card1_content = "<div class='text-primary'>some content</div>"
        this.card2_content = markup("<div class='text-primary'>some content</div>")
        this.state = useState({sum: 0});
    }

    incrementSum() {
        this.state.sum++;
    }

    static components = {Counter, Card, ToDoList};
}
