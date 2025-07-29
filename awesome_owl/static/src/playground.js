/** @odoo-module **/

import { Counter } from './counter/counter';
import { Card } from './card/card';
import { markup, Component, useState} from "@odoo/owl";

export class Playground extends Component {

    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    state = useState({
        cards: [
            { title: "Card 1", content: markup("<p>Dhananjay Brahmane</p>") },
            { title: "Card 2", content: "Content of card 2" }
        ],
        sum: 0
    });

    incrementSum()
    {
       this.state.sum++
    }
    
}
