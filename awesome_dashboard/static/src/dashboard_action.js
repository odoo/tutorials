/** @odoo-module **/

import { Component, onWillStart, useState, useRef, onMounted, useEffect } from "@odoo/owl";
import { loadBundle, LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";

export class LazyComponentLoader extends Component {
    static components = { LazyComponent };
    static template = "awesome_dashboard.LazyComponentLoader";
}

registry.category("actions").add("awesome_dashboard.dashboard_action", LazyComponentLoader);
