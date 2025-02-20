import { Component , useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,Card };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }

    decrement(){
        this.state.value--;
    }
}