/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

/**
 * Reusable hook to auto-focus an input DOM element
 * Usage: call in setup, bind to t-ref element
 */
export function useAutofocus(refName) {
    const ref = useRef(refName);
    onMounted(() => {
        ref.el?.focus(); // safe access after mount
    });
    return ref;
}
