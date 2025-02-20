/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
export class Counter extends Component{
    setup(){
        this.state=useState({value:0});
        }
    increment(){
        this.state.value++;
    }

    static template = "awesome_owl.counter";
}
export class Card extends Component{
static template = "awesome_owl.card"
}
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components={Counter,Card}
    }

