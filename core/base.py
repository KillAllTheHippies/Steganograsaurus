"""Base interfaces for the core steganography module."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

import numpy as np
from PIL import Image


class BaseEncoder(ABC):
    """Abstract base class for steganography encoders."""

    @abstractmethod
    def encode(
        self, cover_image: Union[Image.Image, np.ndarray], data: bytes, **kwargs: Any
    ) -> Union[Image.Image, np.ndarray]:
        """Encode data into a cover image.

        Args:
            cover_image: The cover image to hide data in.
            data: The data to hide.
            **kwargs: Additional encoder-specific parameters.

        Returns:
            The stego image containing the hidden data.
        """
        pass


class BaseDecoder(ABC):
    """Abstract base class for steganography decoders."""

    @abstractmethod
    def decode(
        self, stego_image: Union[Image.Image, np.ndarray], **kwargs: Any
    ) -> bytes:
        """Extract hidden data from a stego image.

        Args:
            stego_image: The stego image containing hidden data.
            **kwargs: Additional decoder-specific parameters.

        Returns:
            The extracted data.
        """
        pass


class BaseSteganographyAlgorithm(ABC):
    """Abstract base class for steganography algorithms."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the algorithm.

        Args:
            config: Optional configuration dictionary.
        """
        self.config = config or {}
        self.encoder = self._create_encoder()
        self.decoder = self._create_decoder()

    @abstractmethod
    def _create_encoder(self) -> BaseEncoder:
        """Create and return the encoder instance."""
        pass

    @abstractmethod
    def _create_decoder(self) -> BaseDecoder:
        """Create and return the decoder instance."""
        pass

    @abstractmethod
    def get_capacity(self, image: Union[Image.Image, np.ndarray]) -> int:
        """Calculate the maximum data capacity for an image.

        Args:
            image: The image to calculate capacity for.

        Returns:
            Maximum number of bytes that can be hidden.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the algorithm name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the algorithm description."""
        pass
