/** @odoo-module */

import { useRef, onMounted } from "@odoo/owl"

export function useAutoFocuse(inputName) {
    const inputRef = useRef(inputName)

    onMounted(() => {
        inputRef.el.focus();
    });
}
