/** @odoo-module **/

import { Component , markup} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card  } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components= { Counter , Card };

    setup(){
        this.str1 = "<div class='text-primary'>Some Content</div>";
        this.str2 = markup("<div class='text-primary'>Not some Content</div>");
    }
}
