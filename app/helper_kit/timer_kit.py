from time import time


class TimerKit:

    events = []

    @staticmethod
    def start_event(event_label: str):

        event_object = {
            "label": event_label
        }

        for event in TimerKit.events:
            if event["label"] == event_label:
                event_object = event

        event_object["start_time"] = time()

        TimerKit.events.append(event_object)

        print("STARTING " + event_label + "... ")

    @staticmethod
    def result(event_label: object) -> str:

        event_object = None

        for event in TimerKit.events:
            if event["label"] == event_label:
                event_object = event

        if event_object is None:
            print("EVENT NOT FOUNT: " + event_label)
            return "EVENT NOT FOUNT: " + event_label
        else:
            final_time = time() - event_object["start_time"]
            print("RESULT FOR " + event_label + " >>>>> " + str(final_time))
            return "RESULT FOR " + event_label + " >>>>> " + str(final_time)