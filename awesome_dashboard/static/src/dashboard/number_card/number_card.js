import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class NumberCard extends Component {
    static template = "awesome_dashboard.numbercard";
    static props = {
        title: { type: String },
        value: { type: [Number, String] },
    };
}
