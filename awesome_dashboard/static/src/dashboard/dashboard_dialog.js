import { Component, useState} from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class AwesomeDashboardDialog extends Component {
    static template = "awesome_dashboard.AwesomeDashboardDialog";
    static components = { Dialog, CheckBox };
    static props = ["items", "close", "updateDisabledItems"];

    setup() {
        this.items = useState(this.props.items.map(item => {
            return {
                ...item,
                checked: !browser.localStorage.getItem("disabledDashboardItems").includes(item.id)
            };
        }));
    }

    toggle(checked, item) {
        item.checked = checked;
    }

    confirm() {
        console.log(this.items);
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.checked
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.updateDisabledItems(newDisabledItems);
        this.props.close();
    }
}