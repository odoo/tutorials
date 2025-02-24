import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

export class DashboardSettings extends Component {

    static template = "awesome_dashboard.DashboardSettings";
    static components = { Dialog };
    static props = {
        confirm: Function,
        close: Function
    };

    setup() {
        this.items = registry.category("awesome_dashboard").getEntries().map(entries => entries[1])
        this.hiddenItems = useState(browser.localStorage.getItem("itemsPreference").split(',') || [])
        this.toggleSetting = this.toggleSetting.bind(this)
    }

    toggleSetting(itemId) {
        if(this.hiddenItems.includes(itemId)){
            this.hiddenItems.splice(0, this.hiddenItems.length, ...this.hiddenItems.filter((item) => item!=itemId))
        }
        else{
            this.hiddenItems.push(itemId)
        }
    }

    apply() {
        browser.localStorage.setItem("itemsPreference", this.hiddenItems)
        this.props.confirm(true)
        this.props.close()
    }
}
