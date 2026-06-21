# ==========================================================
# OpenShell Console
# Event Manager
# ==========================================================

from collections import defaultdict


class EventManager:

    def __init__(self):

        self._subscribers = defaultdict(list)

    # ======================================================
    # SUBSCRIBE
    # ======================================================

    def subscribe(
        self,
        event_name,
        callback
    ):

        self._subscribers[event_name].append(
            callback
        )

    # ======================================================
    # UNSUBSCRIBE
    # ======================================================

    def unsubscribe(
        self,
        event_name,
        callback
    ):

        if event_name not in self._subscribers:
            return

        if callback in self._subscribers[event_name]:

            self._subscribers[event_name].remove(
                callback
            )

    # ======================================================
    # PUBLISH
    # ======================================================

    def publish(
        self,
        event_name,
        payload=None
    ):

        callbacks = self._subscribers.get(
            event_name,
            []
        )

        for callback in callbacks:

            try:

                callback(payload)

            except Exception as e:

                print(
                    f"[EVENT ERROR] {event_name}: {e}"
                )