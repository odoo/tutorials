/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class Card extends Component {
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            }
        }
    }

    setup() {
        this.state = useState({open: true});
    }

    onClickToggle(){
        this.state.open = !this.state.open;
    }

    static template = "awesome_owl.card";

}
