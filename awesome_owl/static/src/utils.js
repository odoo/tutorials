import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(focusText) {
    let inputRef = useRef(focusText);
    onMounted(() => {
        inputRef.el.focus();
    });
    return inputRef;
}