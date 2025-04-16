import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName = "inputfocus") {
    const inputRef = useRef(refName);

    onMounted(() => {
        inputRef.el?.focus(); // Focus the input if it exists
    });

    return inputRef;
}
