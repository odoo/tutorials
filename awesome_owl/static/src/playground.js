/** @odoo-module **/

import { markup, Component , useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    
    static components = { Counter , Card };
    card_content1 = "<div class='text-primary'> card 1 content</div>";
    card_content2 = markup("<div class='text-primary'> card 2 content</div>");

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }

}
