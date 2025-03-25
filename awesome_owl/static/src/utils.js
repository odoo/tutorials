/** @odoo-module **/
import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const elementRef = useRef(refName);
    onMounted(() => {
        elementRef.el.focus();
    });
    return elementRef;
}
