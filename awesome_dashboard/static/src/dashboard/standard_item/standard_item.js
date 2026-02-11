/** @odoo-module **/

import { Component } from "@odoo/owl";

export class StandardItem extends Component {
    static template = "awesome_dashboard.StandardItem";
    static props = {
        title: String,
        value: Number,
    };
}
