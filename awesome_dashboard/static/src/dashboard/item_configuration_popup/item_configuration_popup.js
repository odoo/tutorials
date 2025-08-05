import { Component, useState } from '@odoo/owl'
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class ItemConfigurationPopup extends Component {
    static template = "awesome_dashboard.itemConfigurationDashboard"
    static props = {
        items: {
            type: Object
        },
        itemConfigs: {
            type: Object
        },
        closeWrapper: {
            type: Function
        },
        updateItemConfigCallback: {
            type: Function
        }

    }
    static components = { CheckBox, Dialog }
    static defaultProps = {}
    
    setup() {
        this.state = useState({
            itemConfigs: this.props.itemConfigs
        });
    }

    confirm() {
        this.setBrowserLocalStorageData();
        this.closeWrapper();
    }
    
    toggleItemConfigCard(itemid, checked) {
        this.state.itemConfigs[itemid] = checked;
        this.props.updateItemConfigCallback(this.state.itemConfigs)
    }

    setBrowserLocalStorageData() {
        browser.localStorage.setItem(
            "awesome_dashboard.item_configuration",
            JSON.stringify(this.state.itemConfigs)
        );
    }

    closeWrapper() {
        this.props.closeWrapper();
        this.props.close();
    }
}
