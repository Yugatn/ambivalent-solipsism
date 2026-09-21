use proptest::prelude::*;

use eugene_messenger_domain::{
    clock::{HlcTimestamp, HybridLogicalClock},
    ids::DeviceId,
    swipe::{SwipeDirection, SwipeOutcome, SwipePolicy, SwipeStateMachine},
};

proptest! {
    #[test]
    fn swipe_below_threshold_never_commits(distance in 0.0f32..0.299f32) {
        let mut sm = SwipeStateMachine::new(SwipePolicy::default());
        sm.begin(SwipeDirection::Left);
        sm.drag(distance);
        prop_assert_eq!(sm.release(500), SwipeOutcome::None);
    }

    #[test]
    fn swipe_is_bounded(distance in -10.0f32..10.0f32) {
        let mut sm = SwipeStateMachine::new(SwipePolicy::default());
        sm.begin(SwipeDirection::Right);
        sm.drag(distance);
        let outcome = sm.release(500);
        prop_assert!(matches!(outcome, SwipeOutcome::None | SwipeOutcome::Commit(SwipeDirection::Right)));
    }
}

#[test]
fn hlc_tick_is_monotonic() {
    let device = DeviceId(1);
    let mut clock = HybridLogicalClock::new(device);
    let a = clock.tick(100);
    let b = clock.tick(100);
    let c = clock.tick(99);
    assert!(b >= a);
    assert!(c >= b);
}

#[test]
fn hlc_remote_update_moves_past_remote_timestamp() {
    let device_a = DeviceId(1);
    let device_b = DeviceId(2);
    let mut a = HybridLogicalClock::new(device_a);
    let remote = HlcTimestamp { wall_time_ms: 100, counter: 4, device_id: device_b };
    let updated = a.update(remote, 50);
    assert!(updated > remote);
}
