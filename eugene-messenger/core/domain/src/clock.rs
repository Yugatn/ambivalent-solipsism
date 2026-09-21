use crate::ids::DeviceId;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct HlcTimestamp {
    pub wall_time_ms: u64,
    pub counter: u32,
    pub device_id: DeviceId,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct HybridLogicalClock {
    wall_time_ms: u64,
    counter: u32,
    device_id: DeviceId,
}

impl HybridLogicalClock {
    pub fn new(device_id: DeviceId) -> Self {
        Self {
            wall_time_ms: 0,
            counter: 0,
            device_id,
        }
    }

    pub fn tick(&mut self, now_ms: u64) -> HlcTimestamp {
        if now_ms > self.wall_time_ms {
            self.wall_time_ms = now_ms;
            self.counter = 0;
        } else {
            self.counter = self.counter.saturating_add(1);
        }
        self.snapshot()
    }

    pub fn update(&mut self, remote: HlcTimestamp, now_ms: u64) -> HlcTimestamp {
        let physical = now_ms.max(self.wall_time_ms).max(remote.wall_time_ms);
        let local_at_max = physical == self.wall_time_ms;
        let remote_at_max = physical == remote.wall_time_ms;

        self.counter = match (local_at_max, remote_at_max) {
            (true, true) => self.counter.max(remote.counter).saturating_add(1),
            (true, false) => self.counter.saturating_add(1),
            (false, true) => remote.counter.saturating_add(1),
            (false, false) => 0,
        };
        self.wall_time_ms = physical;
        self.snapshot()
    }

    pub fn snapshot(&self) -> HlcTimestamp {
        HlcTimestamp {
            wall_time_ms: self.wall_time_ms,
            counter: self.counter,
            device_id: self.device_id,
        }
    }
}
