/** 可见性感知的轮询调度 — 标签页隐藏时降频 */

const PollScheduler = (() => {
  const HIDDEN_MULTIPLIER = 3;
  const tasks = new Map();
  let timerId = null;
  let baseIntervalMs = 5 * 60 * 1000;

  function effectiveInterval() {
    if (typeof document !== "undefined" && document.visibilityState === "hidden") {
      return baseIntervalMs * HIDDEN_MULTIPLIER;
    }
    return baseIntervalMs;
  }

  function runDue() {
    const now = Date.now();
    const interval = effectiveInterval();
    tasks.forEach((state, fn) => {
      if (now - state.lastRun >= interval) {
        state.lastRun = now;
        Promise.resolve(fn()).catch((err) => console.warn("poll task failed", err));
      }
    });
  }

  function schedule() {
    if (timerId) clearInterval(timerId);
    timerId = setInterval(runDue, 60 * 1000);
    runDue();
  }

  return {
    configure({ intervalMs } = {}) {
      if (intervalMs) baseIntervalMs = intervalMs;
      schedule();
    },
    register(fn) {
      tasks.set(fn, { lastRun: 0 });
    },
    start() {
      schedule();
      if (typeof document !== "undefined") {
        document.addEventListener("visibilitychange", () => {
          tasks.forEach((s) => {
            s.lastRun = 0;
          });
          runDue();
        });
      }
    },
  };
})();
