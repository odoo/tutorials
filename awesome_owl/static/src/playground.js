/** @odoo-module **/

import { Component , useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    
    static components = { Counter , Card };

}
