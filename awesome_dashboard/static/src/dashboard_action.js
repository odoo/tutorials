/** @odoo-module **/

import { Component,onWillStart,useState,useRef,onMounted,useEffect } from "@odoo/owl";
import { loadBundle, LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import {Layout} from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { loadJS } from "@web/core/assets";

export class LazyComponentLoader extends Component{
    static components = {LazyComponent};
    static template = "awesome_dashboard.LazyComponentLoader";
}
registry.category("actions").add("awesome_dashboard.dashboard_action",LazyComponentLoader);
