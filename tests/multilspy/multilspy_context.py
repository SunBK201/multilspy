"""
Provides the ScubalspyContext class, which stores the context for a Scubalspy test.
"""

import dataclasses

from scubalspy.scubalspy_config import ScubalspyConfig
from scubalspy.scubalspy_logger import ScubalspyLogger


@dataclasses.dataclass
class ScubalspyContext:
    """
    Stores the context for a Scubalspy test.
    """
    config: ScubalspyConfig
    logger: ScubalspyLogger
    source_directory: str