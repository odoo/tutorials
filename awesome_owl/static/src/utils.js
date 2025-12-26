import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(name) {
    let ref = useRef(name);
    onMounted(() => {
        ref.el.focus();
    });
}
