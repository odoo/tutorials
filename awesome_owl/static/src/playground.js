import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./todo/todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};

    setup() {
        this.state = useState({
            content1: markup("<i>This is card-1 content</i>"),
            content2: "<b>This is card-2 content</b>",
            content3: markup("<b><sub>This is </sub> card <sup>3</sup> <sub>content</sub></b>")
        });
        this.sum = useState({value: 0});
    }

    incrementSum(increment) {
        if (increment) {
            this.sum.value++;
        } else {
            this.sum.value--;
        }
    }
}
