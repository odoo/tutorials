export function choose(clicker, rewards) {
    const list = rewards.filter((reward) => {
        if (reward.minLevel && reward.maxLevel) {
            return clicker.level >= reward.minLevel && clicker.level <= reward.maxLevel;
        } else if (reward.minLevel) {
            return clicker.level >= reward.minLevel;
        } else if (reward.maxLevel) {
            return clicker.level <= reward.maxLevel;
        } else {
            return true;
        }
    });

    return list[Math.floor(Math.random() * list.length)];
}
