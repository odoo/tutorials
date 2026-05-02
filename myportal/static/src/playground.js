import { Component, useRef, useState, onWillStart, useEffect, onWillUnmount } from "@odoo/owl";
import { ControlPanel } from "@web/search/control_panel/control_panel"
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";


export class Playground extends Component {
    static template = "myportal.playground";

    //static components = {
    //    Layout,
    //};

    static props = {
    };


    setup() {

    }

}