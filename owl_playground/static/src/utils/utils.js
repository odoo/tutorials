/** @odoo-module **/

import { onMounted } from "@odoo/owl"

export function useAutoFocus(ref) {
    onMounted(() => {
        ref.el.focus();
    });
}
