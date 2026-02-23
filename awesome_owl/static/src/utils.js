// awesome_owl/utils.js
import { onMounted, useRef } from "@odoo/owl";

// Custom hook to autofocus an input by t-ref
export function useAutofocus(refName) {
    const ref = useRef(refName);
    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });
    return ref;
}