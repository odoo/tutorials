import { Component, xml, useState } from "@odoo/owl"

import { Dialog } from "@web/core/dialog/dialog"
import { CheckBox } from "@web/core/checkbox/checkbox"
import { browser } from "@web/core/browser/browser"
import { _t } from "@web/core/l10n/translation"

export class SettingsDialog extends Component {
    static props = {
        items: { type: Array },
        close: { type: Function },
    }

    static components = { Dialog, CheckBox }

    static template = xml`
        <Dialog title="title">
            Which cards do you wish to see?
            <t t-foreach="props.items" t-as="item" t-key="item.id">
                <CheckBox value="!disabled[item.id]" onChange="() => disabled[item.id] = !disabled[item.id]">
                    <t t-esc="item.description"/>
                </CheckBox>
            </t>
            <t t-set-slot="footer">
                <button class="btn btn-primary" t-on-click="onApply">Apply</button>
            </t>
        </Dialog>
    `

    setup() {
        this.title = _t("Dashboard items configuration")
        this.disabled = useState({})
        for (const item of this.props.items) {
            this.disabled[item.id] = item.disabled
        }
    }

    onApply() {
        for (const item of this.props.items) {
            item.disabled = this.disabled[item.id]
        }
        const ids = this.props.items.filter((item) => item.disabled).map((item) => item.id)
        browser.localStorage.setItem("disabled_dashboard_items", JSON.stringify(ids))
        this.props.close()
    }
}
