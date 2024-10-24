/** @odoo-module **/
import {Card} from "./card/card";
import {Counter} from "./counter/counter";
import {TodoList} from "./todos/todoList";
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
        console.log(this.counterSum.value);
        if(this.counterSum.value % 10 === 0){
            let item = document.getElementById("counter-div");
            console.log(item);
            item.classList.add('bigger');
            setTimeout(() => {
                item.classList.remove('bigger');
            },300);
        }
    };

}
