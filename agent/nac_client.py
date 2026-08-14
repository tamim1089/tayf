"""
Nokia Network-as-Code (NaC) SDK v10.0.0 call patterns.

Verified against Nokia's own integration tests earlier in this project's
research pass (not invented syntax). Real usage requires NaC portal
registration (project task #2, still outstanding) to obtain NAC_TOKEN.

Per agent/compliance.md: this module implements the CAMARA API calls only.
Any decision-making LLM layered on top must be Gemini 2.5 or Groq-hosted,
never Claude, and must not be built on MCP.
"""

import os
from dotenv import load_dotenv
from network_as_code.client import NetworkAsCodeApi

load_dotenv()

client = NetworkAsCodeApi(
    api_key=os.environ["NAC_TOKEN"],
    rapidapi_host=os.environ.get("RAPIDAPI_HOST", "network-as-code.nokia.rapidapi.com"),
)
# base_url defaults to https://network-as-code.p-eu.rapidapi.com


def start_qod_session(phone_number: str, public_ip: str, app_server_ip: str, duration_s: int = 60):
    """Request a guaranteed-latency QoD session for one call leg."""
    return client.qod.create_session_v1(
        device={
            "phone_number": phone_number,
            "ipv4Address": {"publicAddress": public_ip, "privateAddress": public_ip},
        },
        application_server={"ipv4address": app_server_ip},
        qos_profile="DOWNLINK_M_UPLINK_L",  # uplink-heavy: TAYF's driving-parameter stream is upload-dominant
        duration=duration_s,
    )


def extend_qod_session(session_id: str, additional_s: int = 60):
    return client.qod.extend_session_v1(session_id=session_id, requested_additional_duration=additional_s)


def end_qod_session(session_id: str):
    client.qod.delete_session_v1(session_id=session_id)


def predict_congestion(phone_number: str):
    """
    Forward-looking congestion prediction for the UPCOMING 15 MINUTES —
    this is what makes agent/README.md's loop genuinely agentic (act before
    congestion hits) rather than a reactive QoS thermostat.

    Returns: {timeIntervalStart, timeIntervalStop, congestionLevel: Low|Medium|High,
              confidenceLevel: 0-100}
    """
    return client.congestion_insights.query(device={"phone_number": phone_number})


def create_demo_slice(mcc: str, mnc: str, slice_name: str, guaranteed_kbps: int, max_kbps: int):
    """Network slice for a scheduled high-value session (e.g. a live demo)."""
    result = client.slice.create_slice(
        network_identifier={"mcc": mcc, "mnc": mnc},
        slice_info={"service_type": "eMBB", "differentiator": "444444"},
        name=slice_name,  # must match ^[a-zA-Z0-9][a-zA-Z0-9-]{3,63}[a-zA-Z0-9]$
        slice_uplink_throughput={"guaranteed": guaranteed_kbps, "maximum": max_kbps},
        device_uplink_throughput={"guaranteed": guaranteed_kbps, "maximum": max_kbps},
        max_data_connections=10,
        max_devices=5,
    )
    client.slice.activate(id=result.name)
    return result


def attach_device_to_slice(phone_number: str, imsi: int, slice_id: str, app_id: str, app_names: list):
    return client.slice.attach_device(
        device={"phone_number": phone_number, "imsi": imsi},  # both mandatory
        slice_id=slice_id,
        traffic_categories={"apps": {"os": app_id, "apps": app_names}},
    )
