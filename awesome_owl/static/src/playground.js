/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    static props = {}

    setup() {
        this.sum = useState({ value: 0 });
        this.incrementSum = () => {
            this.sum.value++;
        };

        this.activeTab = useState({ value: 'All' });
        this.setActiveTab = (tab) => {
            this.activeTab.value = tab;
        };

        onMounted(() => {
            let style = document.createElement("style");
            style.innerHTML = `::-webkit-scrollbar {display: none;}`;
            document.head.appendChild(style);
        });
    }
}
