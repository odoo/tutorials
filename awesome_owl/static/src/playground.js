/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./Counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = {Counter};
    
    setup(){
        this.state = useState({count: 0});
    }
}
