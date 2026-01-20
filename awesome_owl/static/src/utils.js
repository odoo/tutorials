import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName = "inputfocus") {
    const inputRef = useRef(refName);

    onMounted(() => {
        inputRef.el?.focus();
    });

    return inputRef;
}
