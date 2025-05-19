import {Component, markup, useState} from "@odoo/owl"
import { Counter } from "./counter/counter"
import { Card } from "./card/card"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    setup() {
        this.state = useState({value:0})
        this.cards = [
            {
                title: "mayur1",
                content: "this is normal <strong> Name </strong> ok",
            },
            {
                title: "mayur2",
                content: markup("this is normal <strong> Name </strong> ok"),
            }
        ];
    }
    incrementSum() {
        this.state.value++;
    }
    static components = { Counter,Card };
}
