import { Component, useState} from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry }  from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import {CheckBox} from "@web/core/checkbox/checkbox";

export class SettingsDialog extends Component
{
    static template = "awesome_dashboard.SettingsDialog";
    static components = {Dialog, CheckBox}
    static props = ['close','disabled','items','OnChange'];

    setup()
    {
        console.log(this.props.disabled);
        this.items = useState(this.props.items.map((item) =>
            {
                return {
                    ...item,
                    enabled: !this.props.disabled.includes(item.id),
                }
            }))
    }
    done()
    {
        this.props.close();
    }
    onChange(state, item)
    {
        item.enabled = state;
        const updateDisabled = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem("disabledDashboardItems",updateDisabled);
        this.props.OnChange(updateDisabled);
    }
}
