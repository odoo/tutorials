import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(refName = "input") {
    const inputRef = useRef(refName);

    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });

    return inputRef;
}