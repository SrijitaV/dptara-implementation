
class LoadPredictor:
    """
    Predicts future resource utilization using historical
    observations and simple linear regression.

    Utilization is represented as a ratio between 0 and 1.

    Note:
        Linear regression is a configurable implementation
        choice. It should not be described as the exact
        prediction method proposed in the research paper
        unless verified from the paper.
    """

    def __init__(self, max_history=50):

        if not isinstance(max_history, int) or max_history < 2:
            raise ValueError(
                "max_history must be an integer greater than or equal to 2."
            )

        self.max_history = max_history
        self.history = {}

    def record_observation(self, resource_id, time, utilization):
        """
        Store a historical resource utilization observation.
        """

        if not resource_id:
            raise ValueError("Invalid resource ID.")

        time = float(time)
        utilization = float(utilization)

        if time < 0:
            raise ValueError("Observation time cannot be negative.")

        if not 0 <= utilization <= 1:
            raise ValueError(
                "Utilization must be between 0 and 1."
            )

        if resource_id not in self.history:
            self.history[resource_id] = []

        observations = self.history[resource_id]

        observations.append((time, utilization))

        # Keep only the most recent observations.
        if len(observations) > self.max_history:
            observations.pop(0)

    def predict_load(self, resource_id, future_time):
        """
        Predict future utilization using simple linear regression.

        Returns:
            Predicted utilization between 0 and 1.
        """

        if resource_id not in self.history:
            raise ValueError(
                "No historical data for this resource."
            )

        future_time = float(future_time)

        if future_time < 0:
            raise ValueError(
                "Future time cannot be negative."
            )

        observations = self.history[resource_id]

        if not observations:
            raise ValueError(
                "No observations available for this resource."
            )

        # With fewer than two observations, use the latest value.
        if len(observations) < 2:
            return observations[-1][1]

        times = [observation[0] for observation in observations]
        loads = [observation[1] for observation in observations]

        mean_time = sum(times) / len(times)
        mean_load = sum(loads) / len(loads)

        # Calculate linear regression slope.
        numerator = sum(
            (time - mean_time) * (load - mean_load)
            for time, load in observations
        )

        denominator = sum(
            (time - mean_time) ** 2
            for time in times
        )

        # Avoid division by zero when all observation times are equal.
        if denominator == 0:
            return mean_load

        slope = numerator / denominator

        # Predict utilization at the requested future time.
        predicted_load = (
            mean_load
            + slope * (future_time - mean_time)
        )

        # Utilization must remain within [0, 1].
        predicted_load = max(
            0.0,
            min(1.0, predicted_load)
        )

        return predicted_load
