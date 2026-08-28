import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


export class MyDialog extends Component {
    static template = "awesome_dashboard.mydialog";

    static components = {
        Dialog,
        CheckBox
    }

    static props = {
        disabledItems: Object,
        updateConfiguration: Function,
        items: Array,
        close: Function
    }

    setup() {
        console.log(this.props)
    }

    onChange(ev, item) {
        // this.disabledItems[item.id] = ev
        this.props.disabledItems[item.id] = ev
    }

    done() {
        browser.localStorage.setItem("disabledDashboardItems", JSON.stringify(this.props.disabledItems))
        this.props.updateConfiguration(this.props.disabledItems)
        this.props.close()
    }
}