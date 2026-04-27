import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(named_ref) {
    const ref = useRef(named_ref);
    onMounted(() => {
        ref.el.focus();
    });
}
