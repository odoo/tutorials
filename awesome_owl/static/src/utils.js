import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName) {
    if (!refName) {
        return;
    }
    const ref = useRef(refName);
    onMounted(() => {
        ref.el.focus();
    });
}