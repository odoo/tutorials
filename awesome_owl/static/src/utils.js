import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(refName) {
    let inputRef = useRef(refName);
    onMounted(() => {
        inputRef.el?.focus();
    });
}
