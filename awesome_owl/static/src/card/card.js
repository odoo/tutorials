/** @odoo-module **/

import {Component} from "@odoo/owl";

export class Card extends Component {
    static props = ['title','content']


    static template = "awesome_owl.card";

}
