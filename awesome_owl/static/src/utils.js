import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocusInput(refName) {
	const inputRef = useRef(refName);
	onMounted(() => {
		inputRef.el.focus();
	})
}
