import { onMounted } from "@odoo/owl";

export function useAutoFocus(refName) {
    onMounted(() => {
        refName.el.focus();
    })
}