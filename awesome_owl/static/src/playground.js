import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter"
import {Card} from "./card/card"
import {TodoList} from "./TodoList/TodoList"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}

    setup() {
        this.state = useState({
                sum: 0
            }
        )
        this.safeHtml = markup("<div class='text-success fw-bold'>some content</div>");
        this.withoutMarkup = "<div class='text-danger'>without markup</div>"
    }

    incrementSum(decrement) {
        if (decrement) {
            this.state.sum--;
        } else {
            this.state.sum++;
        }
    }
}
