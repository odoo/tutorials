/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components= {Counter, Card, TodoList};

    setup(){
        this.safehtml= markup("<strong>This is bold HTML content</strong>");
        this.escapedText= "<strong>This is bold HTML content</strong>";
        this.sum= useState({value:0})
    }
    incrementSum(){
        this.sum.value++;
    }
}
