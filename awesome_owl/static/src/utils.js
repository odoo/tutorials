import { useRef, onMounted } from "@odoo/owl";

export const useAutoFocus = () => {
    const inputRef = useRef("focus-input");
    onMounted(() => {
        inputRef.el?.focus();
    })
}