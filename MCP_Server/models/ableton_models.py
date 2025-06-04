"""Data models for Ableton Live integration."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class DeviceType(Enum):
    """Device type enumeration."""

    INSTRUMENT = "instrument"
    AUDIO_EFFECT = "audio_effect"
    MIDI_EFFECT = "midi_effect"
    DRUM_MACHINE = "drum_machine"
    RACK = "rack"
    UNKNOWN = "unknown"


class CommandType(Enum):
    """Command type enumeration for Ableton commands."""

    GET_SESSION_INFO = "get_session_info"
    GET_TRACK_INFO = "get_track_info"
    CREATE_MIDI_TRACK = "create_midi_track"
    CREATE_AUDIO_TRACK = "create_audio_track"
    SET_TRACK_NAME = "set_track_name"
    CREATE_CLIP = "create_clip"
    ADD_NOTES_TO_CLIP = "add_notes_to_clip"
    SET_CLIP_NAME = "set_clip_name"
    SET_TEMPO = "set_tempo"
    FIRE_CLIP = "fire_clip"
    STOP_CLIP = "stop_clip"
    START_PLAYBACK = "start_playback"
    STOP_PLAYBACK = "stop_playback"
    LOAD_INSTRUMENT_OR_EFFECT = "load_instrument_or_effect"
    LOAD_BROWSER_ITEM = "load_browser_item"
    GET_BROWSER_TREE = "get_browser_tree"
    GET_BROWSER_ITEMS_AT_PATH = "get_browser_items_at_path"


@dataclass
class Note:
    """MIDI note data model."""

    pitch: int
    start_time: float
    duration: float
    velocity: int = 100
    mute: bool = False

    def to_live_format(self) -> tuple:
        """Convert to Ableton Live's note format."""
        return (self.pitch, self.start_time, self.duration, self.velocity, self.mute)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        """Create Note from dictionary."""
        return cls(
            pitch=data.get("pitch", 60),
            start_time=data.get("start_time", 0.0),
            duration=data.get("duration", 0.25),
            velocity=data.get("velocity", 100),
            mute=data.get("mute", False),
        )


@dataclass
class ClipInfo:
    """Clip information data model."""

    name: str
    length: float
    is_playing: bool = False
    is_recording: bool = False
    has_clip: bool = True

    @classmethod
    def from_ableton_clip(cls, clip) -> "ClipInfo":
        """Create ClipInfo from Ableton clip object."""
        return cls(
            name=clip.name,
            length=clip.length,
            is_playing=clip.is_playing,
            is_recording=clip.is_recording,
        )


@dataclass
class DeviceInfo:
    """Device information data model."""

    index: int
    name: str
    class_name: str
    device_type: DeviceType = DeviceType.UNKNOWN

    @classmethod
    def from_ableton_device(cls, device, index: int) -> "DeviceInfo":
        """Create DeviceInfo from Ableton device object."""
        device_type = DeviceType.UNKNOWN

        # Simple heuristic to determine device type
        try:
            if hasattr(device, "can_have_drum_pads") and device.can_have_drum_pads:
                device_type = DeviceType.DRUM_MACHINE
            elif hasattr(device, "can_have_chains") and device.can_have_chains:
                device_type = DeviceType.RACK
            elif hasattr(device, "class_display_name"):
                class_name_lower = device.class_display_name.lower()
                if "instrument" in class_name_lower:
                    device_type = DeviceType.INSTRUMENT
                elif "audio_effect" in device.class_name.lower():
                    device_type = DeviceType.AUDIO_EFFECT
                elif "midi_effect" in device.class_name.lower():
                    device_type = DeviceType.MIDI_EFFECT
        except Exception:
            pass

        return cls(
            index=index,
            name=device.name,
            class_name=device.class_name,
            device_type=device_type,
        )


@dataclass
class ClipSlotInfo:
    """Clip slot information data model."""

    index: int
    has_clip: bool
    clip: ClipInfo | None = None


@dataclass
class TrackInfo:
    """Track information data model."""

    index: int
    name: str
    is_audio_track: bool
    is_midi_track: bool
    mute: bool = False
    solo: bool = False
    arm: bool = False
    volume: float = 0.85
    panning: float = 0.0
    clip_slots: list[ClipSlotInfo] = None
    devices: list[DeviceInfo] = None

    def __post_init__(self) -> None:
        if self.clip_slots is None:
            self.clip_slots = []
        if self.devices is None:
            self.devices = []


@dataclass
class MasterTrackInfo:
    """Master track information data model."""

    name: str = "Master"
    volume: float = 0.85
    panning: float = 0.0


@dataclass
class SessionInfo:
    """Session information data model."""

    tempo: float
    signature_numerator: int
    signature_denominator: int
    track_count: int
    return_track_count: int
    master_track: MasterTrackInfo

    @classmethod
    def from_ableton_song(cls, song) -> "SessionInfo":
        """Create SessionInfo from Ableton song object."""
        return cls(
            tempo=song.tempo,
            signature_numerator=song.signature_numerator,
            signature_denominator=song.signature_denominator,
            track_count=len(song.tracks),
            return_track_count=len(song.return_tracks),
            master_track=MasterTrackInfo(
                volume=song.master_track.mixer_device.volume.value,
                panning=song.master_track.mixer_device.panning.value,
            ),
        )


@dataclass
class BrowserItem:
    """Browser item data model."""

    name: str
    uri: str | None = None
    path: str | None = None
    is_folder: bool = False
    is_device: bool = False
    is_loadable: bool = False
    children: list["BrowserItem"] = None

    def __post_init__(self) -> None:
        if self.children is None:
            self.children = []

    @classmethod
    def from_ableton_item(cls, item) -> "BrowserItem":
        """Create BrowserItem from Ableton browser item."""
        return cls(
            name=item.name if hasattr(item, "name") else "Unknown",
            uri=item.uri if hasattr(item, "uri") else None,
            is_folder=hasattr(item, "children") and bool(item.children),
            is_device=hasattr(item, "is_device") and item.is_device,
            is_loadable=hasattr(item, "is_loadable") and item.is_loadable,
        )


@dataclass
class CommandRequest:
    """Command request data model."""

    command_type: CommandType
    params: dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.params is None:
            self.params = {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        return {"type": self.command_type.value, "params": self.params}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CommandRequest":
        """Create CommandRequest from dictionary."""
        command_type_str = data.get("type", "")
        try:
            command_type = CommandType(command_type_str)
        except ValueError:
            raise ValueError(f"Unknown command type: {command_type_str}")

        return cls(command_type=command_type, params=data.get("params", {}))


@dataclass
class CommandResponse:
    """Command response data model."""

    status: str
    result: dict[str, Any] | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        response = {"status": self.status}
        if self.result is not None:
            response["result"] = self.result
        if self.message is not None:
            response["message"] = self.message
        return response

    @classmethod
    def success(cls, result: dict[str, Any] = None) -> "CommandResponse":
        """Create a success response."""
        return cls(status="success", result=result or {})

    @classmethod
    def error(cls, message: str) -> "CommandResponse":
        """Create an error response."""
        return cls(status="error", message=message)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CommandResponse":
        """Create CommandResponse from dictionary."""
        return cls(
            status=data.get("status", "unknown"),
            result=data.get("result"),
            message=data.get("message"),
        )
