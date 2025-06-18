/** @odoo-module **/

import { markup,Component,useState} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,Card };
    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum(value) {
        this.state.sum += value;
    }
    val1 = "<div class='text-primary'>some text 1</div>";
    content = markup("<div class='text-primary'>some text 2</div>");
}
