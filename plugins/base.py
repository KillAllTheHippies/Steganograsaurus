"""Base plugin interface for the plugin system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BasePlugin(ABC):
    """Abstract base class for all plugins."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the plugin.

        Args:
            config: Optional configuration dictionary.
        """
        self.config = config or {}
        self._enabled = True

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the plugin version."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the plugin description."""
        pass

    @property
    def enabled(self) -> bool:
        """Check if the plugin is enabled."""
        return self._enabled

    def enable(self) -> None:
        """Enable the plugin."""
        self._enabled = True
        self.on_enable()

    def disable(self) -> None:
        """Disable the plugin."""
        self._enabled = False
        self.on_disable()

    def on_enable(self) -> None:  # noqa: B027
        """Called when the plugin is enabled."""
        pass

    def on_disable(self) -> None:  # noqa: B027
        """Called when the plugin is disabled."""
        pass

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin.

        Returns:
            True if initialization was successful, False otherwise.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass


class AlgorithmPlugin(BasePlugin):
    """Base class for steganography algorithm plugins."""

    @abstractmethod
    def get_algorithm_class(self) -> type:
        """Return the algorithm class.

        Returns:
            The algorithm class that implements BaseSteganographyAlgorithm.
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Return supported image formats.

        Returns:
            List of supported format extensions (e.g., ['.png', '.jpg']).
        """
        pass


class FilterPlugin(BasePlugin):
    """Base class for image filter plugins."""

    @abstractmethod
    def apply_filter(self, image: Any, **kwargs: Any) -> Any:
        """Apply the filter to an image.

        Args:
            image: The input image.
            **kwargs: Additional filter parameters.

        Returns:
            The filtered image.
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get filter parameters.

        Returns:
            Dictionary of parameter names and their default values.
        """
        pass
