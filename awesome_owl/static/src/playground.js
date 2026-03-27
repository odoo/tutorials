import { Component, useState, onMounted } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";
import { Practice } from "./practice/practice";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList, Practice }

    setup() {
        this.total_card_sum = useState({value: 0})
        this.total_counter_sum = useState({value: 0})
    }

    increasetotal = (clicks) => {
        if(clicks){
            this.total_card_sum.value -= clicks;
        }
        else{
            this.total_card_sum.value++;
        }
    }

    onChange = (counter) => {
        if(counter) this.total_counter_sum.value--;
        else this.total_counter_sum.value++;
    }

    addToTotal = (value) => {
        this.total_counter_sum.value += value;
    }

}
