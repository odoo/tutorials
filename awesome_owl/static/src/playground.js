/** @odoo-module **/

import { Component, markup, useState,onPatched, onWillPatch, onMounted } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";
// import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    setup() {

        this.html1 = markup("<div> Devang Rathod </div>");
        this.html2 = "<div> Devang Rathod </div>";
        this.sum = useState({value: 0});
        this.state = useState({ showPopup: false });
        onMounted(() => {
            console.log("Component has been mounted!");
        });

        onWillPatch(() => {
            console.log("DOM is about to be updated!");
        });

        onPatched(() => {
            console.log("DOM has been updated!");
        });    
    }

    togglePopup() {
        this.state.showPopup = !this.state.showPopup;
    }

    incrementSum(){
        this.sum.value++;
    }
    static components = { Counter, Card, TodoList};
}
