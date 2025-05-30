import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName) {
    var inputRef = useRef(refName);
    onMounted(() => {
        inputRef.el.focus();
    });
}
