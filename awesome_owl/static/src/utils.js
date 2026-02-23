import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName) {
    const targetRef = useRef(refName);
    onMounted(() => {
        targetRef.el.focus();
    });
}
