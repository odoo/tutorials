const { useState } = owl;
import { useService } from "@web/core/utils/hooks";

export function useClicker() {
    return useState(useService('clicker'))
}