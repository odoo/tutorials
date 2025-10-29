import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(refName) {
    let elementRef = useRef(refName);
    onMounted(() => {
        elementRef.el.focus();
    });
    return elementRef;
}
