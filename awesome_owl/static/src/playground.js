/** @odoo-module **/
import {Card} from "./card/card";
import {Counter} from "./counter/counter";
import {TodoList} from "./todoList/todoList";
import {Component, useState} from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};
    static props = {};

    setup() {
        this.counterSum = useState({value: 0});
    };

    incrementSum() {
        this.counterSum.value++;
    };

}
