/** @odoo-module **/

import {Component} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        slots: {
            type: Object,
            shape: {
                title: {type: Object, optional: true},
                footer: {type: Object, optional: true},
                header: {type: Object, optional: true},
                default: {type: Object},
            },
        },
    };


}