/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class Card extends Component {
    static template = 'awesome_owl.card';
    static components = { Counter }

    setup(){
        this.showLessVar = useState(
            { 
            value:false
            }
        );
    }

    showLess() {
        this.showLessVar.value = !this.showLessVar.value;
    }
}
