import { useRef, onMounted } from "@odoo/owl";
export const useAutoFocus = () => {
    const inputRef = useRef("input-autofocus");
    onMounted(() => {
        inputRef.el?.focus();
    })
}
