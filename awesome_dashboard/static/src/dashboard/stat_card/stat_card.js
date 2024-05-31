/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class StatCard extends Component {
    static template = "awesome_dashboard.StatCard";
    static props = {
        title: { type: String },
        data: { type: Number }
    };
}