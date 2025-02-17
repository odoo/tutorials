// utils.js
import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const inputRef = useRef(refName);

    onMounted(() => {
        inputRef.el.focus();
    });

    return inputRef;
}
