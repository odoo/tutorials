/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import {Counter} from "../counter/counter"

export class Card extends Component {
    static template = "awesome_owl.card";
    static components = { Counter };
    
    static props = { title: {type: String}}

    setup(){
      this.state = useState({cardBody:true})
    };

    toggle(){
      this.state.cardBody = !this.state.cardBody;
    };
}
