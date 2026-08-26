import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions"


export async function _loadStatistics() {
    const result = await rpc("/awesome_dashboard/statistics")
    return result
}

export const myCaching = {
        start(env) {
            const memoLoadStatistics = memoize(_loadStatistics)
            return { 
                loadStatistics() {
                    return memoLoadStatistics()
                }
            }
        },
    }

registry.category("services").add("myCaching", myCaching);