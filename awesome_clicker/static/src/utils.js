export function chooseReward(rewards, level) {
    var filtered = rewards.filter((el) => (el.minLevel ?? 0) <= level <= (el.maxLevel ?? Infinity))
    if (filtered.length == 0) {
        return false;
    }
    return filtered[Math.floor(Math.random() * filtered.length)];
}
