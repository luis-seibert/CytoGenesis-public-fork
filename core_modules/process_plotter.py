"""Core module for generating and displaying process parameter plots."""

import os

import matplotlib.backends.backend_agg as agg
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pygame

from core_modules.process_tracker import ProcessTracker


class ProcessPlotter:
    """Class to generate and display process parameter plots.

    Args:
        plot_size (tuple[int, int]): Size of the plot in pixels (width, height).
    """

    def __init__(self, plot_size: tuple[int, int] = (4, 3)) -> None:
        self.plot_size = plot_size
        self.dpi = 80
        self.pixel_font_path = os.path.join(os.getcwd(), "assets", "fonts", "Grand9K Pixel.ttf")
        self._setup_pixel_font()

        plt.style.use("fast")
        plt.rcParams["path.simplify"] = True
        plt.rcParams["path.simplify_threshold"] = 0.1
        plt.rcParams["agg.path.chunksize"] = 10000

        self._max_data_points = 30
        self._update_counter = 0
        self._last_data_hash = None

    def create_simple_plot(self, process_tracker: ProcessTracker) -> pygame.Surface | None:
        """Create a simple plot showing process parameters.

        Args:
            process_tracker (ProcessTracker): Tracker containing process data.

        Returns:
            pygame.Surface | None: Pygame surface containing the plot, or None if no data.
        """

        data = process_tracker.get_data_dict()

        if not data["timestamps"]:
            return None

        current_data_hash = hash(
            (
                len(data["timestamps"]),
                (
                    tuple(data["timestamps"][-5:])
                    if len(data["timestamps"]) >= 5
                    else tuple(data["timestamps"])
                ),
                (
                    tuple(data["total_biomass"][-5:])
                    if len(data["total_biomass"]) >= 5
                    else tuple(data["total_biomass"])
                ),
                (
                    tuple(data["growth_rate"][-5:])
                    if len(data["growth_rate"]) >= 5
                    else tuple(data["growth_rate"])
                ),
            )
        )

        if current_data_hash == self._last_data_hash:
            return None

        self._last_data_hash = current_data_hash

        data = self._downsample_data(data)

        try:
            fig, ax1 = plt.subplots(figsize=self.plot_size, dpi=self.dpi)
            fig.patch.set_facecolor("#ffffffff")

            timestamps = data["timestamps"]

            ax1.plot(
                timestamps,
                data["total_biomass"],
                color="#57a800",
                linewidth=2.0,
                label="Biomass",
                alpha=0.9,
            )
            ax1.set_xlabel(
                "Time (s)", fontsize=12, color="black", weight="medium", fontfamily=self.font_family
            )
            ax1.set_ylabel(
                "Total Biomass",
                fontsize=12,
                color="#57a800",
                weight="medium",
                fontfamily=self.font_family,
            )
            ax1.tick_params(axis="y", colors="#57a800", labelsize=10)
            ax1.tick_params(axis="x", colors="black", labelsize=10)

            self._configure_axis_fonts(ax1)

            ax2 = ax1.twinx()

            smoothed_growth_rate = self._smooth_data(data["growth_rate"], window=10)

            if len(smoothed_growth_rate) > 1:
                ax2.plot(
                    timestamps,
                    smoothed_growth_rate,
                    color="#cb2500",
                    linestyle="--",
                    linewidth=1.8,
                    alpha=0.8,
                    label="Specific Growth Rate",
                )
            else:
                ax2.plot(
                    timestamps,
                    smoothed_growth_rate,
                    color="#cb2500",
                    linestyle="--",
                    linewidth=1.8,
                    alpha=0.8,
                    label="Specific Growth Rate",
                )
            ax2.set_ylabel(
                "Specific Growth Rate",
                fontsize=12,
                color="#cb2500",
                weight="medium",
                fontfamily=self.font_family,
            )
            ax2.tick_params(axis="y", colors="#cb2500", labelsize=10)

            ax3 = ax1.twinx()
            ax3.spines["right"].set_position(("outward", 60))
            ax3.plot(
                timestamps,
                data["total_substrate"],
                color="#0043b6",
                linestyle="-",
                linewidth=2.5,
                alpha=0.85,
                label="Substrate",
                marker="^",
                markersize=2,
                markevery=max(1, len(timestamps) // 15),
            )
            ax3.set_ylabel(
                "Total Substrate",
                fontsize=12,
                color="#0043b6",
                weight="medium",
                fontfamily=self.font_family,
            )
            ax3.tick_params(axis="y", colors="#0043b6", labelsize=10)

            ax1.set_title(
                "Process Parameters",
                fontsize=16,
                color="black",
                weight="bold",
                pad=20,
                fontfamily=self.font_family,
            )
            ax1.grid(True, alpha=0.25, linewidth=0.8, linestyle="-", color="#2B2B2B")

            self._configure_axis_fonts(ax1)
            self._configure_axis_fonts(ax2)
            self._configure_axis_fonts(ax3)

            for ax in [ax1, ax2, ax3]:
                for spine in ax.spines.values():
                    spine.set_color("#3E3E3E")

            plt.tight_layout()
            plt.subplots_adjust(right=0.70)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()
            surface = pygame.image.fromstring(raw_data, size, "RGB")

            plt.close(fig)

            return surface

        except Exception as e:
            print(f"Error creating process parameter plot: {e}")
            try:
                plt.close("all")
            except Exception:
                pass

            return None

    def reset_cache(self) -> None:
        """Reset the internal cache to force plot regeneration on next call."""

        self._last_data_hash = None

    def _setup_pixel_font(self) -> None:
        """Set up the pixel font for matplotlib plots."""

        try:
            if os.path.exists(self.pixel_font_path):
                fm.fontManager.addfont(self.pixel_font_path)
                font_prop = fm.FontProperties(fname=self.pixel_font_path)
                self.font_family = font_prop.get_name()

                plt.rcParams["font.family"] = self.font_family
                plt.rcParams["font.sans-serif"] = [self.font_family] + plt.rcParams[
                    "font.sans-serif"
                ]
            else:
                print(
                    f"Warning: Pixel font not found at {self.pixel_font_path}, using default font"
                )
                self.font_family = "sans-serif"
        except Exception as e:
            print(f"Error setting up pixel font: {e}, using default font")
            self.font_family = "sans-serif"

    def _downsample_data(self, data: dict[str, list]) -> dict[str, list]:
        """Downsample data to improve performance while maintaining visual quality.

        Args:
            data (Dict[str, List]): Raw data from process tracker.

        Returns:
            Dict[str, List]: Downsampled data.
        """

        if not data["timestamps"] or len(data["timestamps"]) <= self._max_data_points:
            return data

        total_points = len(data["timestamps"])

        if total_points <= 2:
            return data

        indices_to_keep = [0]

        intermediate_points = self._max_data_points - 2
        if intermediate_points > 0:
            step = max(1, (total_points - 2) / intermediate_points)
            for i in range(1, intermediate_points + 1):
                index = min(int(i * step), total_points - 2)
                if index not in indices_to_keep:
                    indices_to_keep.append(index)

        if total_points - 1 not in indices_to_keep:
            indices_to_keep.append(total_points - 1)

        indices_to_keep.sort()

        downsampled_data = {}
        for key, values in data.items():
            downsampled_data[key] = [values[i] for i in indices_to_keep]

        return downsampled_data

    def _configure_axis_fonts(self, ax, tick_label_size: int = 10) -> None:
        """Configure pixel font for axis tick labels.

        Args:
            ax: The matplotlib axis object.
            tick_label_size (int): Size of tick labels.
        """

        for label in ax.get_xticklabels():
            label.set_fontfamily(self.font_family)
            label.set_fontsize(tick_label_size)
        for label in ax.get_yticklabels():
            label.set_fontfamily(self.font_family)
            label.set_fontsize(tick_label_size)

    def _smooth_data(self, data: list[float], window: int = 5) -> list[float]:
        """Apply smoothing to data using exponential moving average with outlier removal.

        Args:
            data (list[float]): Data to smooth.
            window (int): Size of the smoothing window.

        Returns:
            list[float]: Smoothed data.
        """

        if len(data) < 2:
            return data

        cleaned_data = []
        for i, value in enumerate(data):
            if i == 0:
                cleaned_data.append(value)
            else:
                prev_value = cleaned_data[i - 1]
                if abs(value - prev_value) > abs(prev_value) * 2.0:
                    dampened = prev_value + (value - prev_value) * 0.3
                    cleaned_data.append(dampened)
                else:
                    cleaned_data.append(value)

        smoothed = [cleaned_data[0]]
        alpha = 2.0 / (window + 1)

        for i in range(1, len(cleaned_data)):
            smoothed_value = alpha * cleaned_data[i] + (1 - alpha) * smoothed[i - 1]
            smoothed.append(smoothed_value)

        return smoothed
