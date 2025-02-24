/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";

export class Numbercard extends Component {
    static template = "awesome_dashboard.number_card";
    static props = {
        itemProps: { type: Object, elements: { title: String, value: Number } }
    }
}
