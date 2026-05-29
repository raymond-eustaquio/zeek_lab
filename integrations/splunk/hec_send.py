#!/usr/bin/env python3

class SplunkHECSender:
    """
    Future Splunk HTTP Event Collector (HEC) sender.

    Planned features:
    - Send Zeek logs as JSON events
    - Batch events for performance
    - Handle retries and failures
    """

    def __init__(self, hec_url: str, hec_token: str):
        self.hec_url = hec_url
        self.hec_token = hec_token

    def send_event(self, event: dict):
        """Placeholder for sending a single event to Splunk HEC."""
        raise NotImplementedError("HEC event sending not implemented yet.")
