import { Component } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import dashboard_items from "../dashboard_items";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { CheckBox, Dialog };
    static props = {
      items: Array,
      close: Function,
      enabled_items: Array,
      setEnabledItems: Function,
    };

    setup() {
        this.all_items = this.props.enabled_items;
    }

    toggleValue(item) {
        if (this.all_items.includes(item)) {
          this.all_items = this.all_items.filter(name => name !== item);
        } else {
            this.all_items = [...this.all_items, item];
        }
    }

    onApply() {
        this.props.setEnabledItems(this.all_items);
        this.props.close();
    }
}
