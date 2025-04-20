from numba import njit


@njit
def update_nutrient_value(
    nutrient_value,
    energy_value,
    growth,
    energy_consumption_rate_maximum,
    energy_affinity,
    division_threshold,
):
    """Updates the nutrient value of the hexagon with mass preservation.

    The nutrient value is updated based on the cell's energy consumption rate and nutrient
    affinity with the Monod equation. The cell absorbs only as much nutrient as needed
    without exceeding the division threshold.

    Args:
        nutrient_value (float): The current nutrient value of the hexagon.
        energy_value (float): The current energy value of the cell.
        growth (bool): Whether the cell is growing or not.
        energy_consumption_rate_maximum (float): The maximum energy consumption rate of the cell.
        energy_affinity (float): The affinity of the cell for energy.
        division_threshold (float): The threshold for cell division.

    Returns:
        tuple: Updated nutrient value, energy value, and growth status.
    """

    if not growth or nutrient_value <= 0:
        return nutrient_value, energy_value, growth

    nutrient_uptake = (
        energy_consumption_rate_maximum
        * nutrient_value
        / (nutrient_value + energy_affinity)
    )

    nutrient_uptake = min(nutrient_uptake, nutrient_value)
    max_possible_uptake = division_threshold - energy_value
    nutrient_uptake = min(nutrient_uptake, max_possible_uptake)

    nutrient_value -= nutrient_uptake
    energy_value += nutrient_uptake

    if abs(nutrient_value) < 0.005:
        nutrient_value = 0
        growth = False

    return nutrient_value, energy_value, growth
