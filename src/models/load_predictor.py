
class LoadPredictor:
    """
    Predicts future resource utilization using
    historical load observations and linear regression.
    """

    def __init__(self, max_history=50):
        self.max_history = max_history
        self.history = {}

    def record_observation(self, resource_id, time, utilization):
        """
        Store historical resource utilization.
        """

        if not 0 <= utilization <= 1:
            raise ValueError("Utilization must be between 0 and 1.")

        if resource_id not in self.history:
            self.history[resource_id] = []

        observations = self.history[resource_id]

        observations.append((float(time), float(utilization)))

        if len(observations) > self.max_history:
            observations.pop(0)

    def predict_load(self, resource_id, future_time):
        """
        Predict future utilization using simple linear regression.
        """

        if resource_id not in self.history:
            raise ValueError("No historical data for this resource.")

        observations = self.history[resource_id]

        if len(observations) < 2:
            return observations[-1][1]

        times = [x[0] for x in observations]
        loads = [x[1] for x in observations]

        mean_time = sum(times) / len(times)
        mean_load = sum(loads) / len(loads)

        numerator = sum(
            (t - mean_time) * (l - mean_load)
            for t, l in observations
        )

        denominator = sum(
            (t - mean_time) ** 2
            for t in times
        )

        if denominator == 0:
            return mean_load

        slope = numerator / denominator

        predicted = mean_load + slope * (
            future_time - mean_time
        )

        return max(0.0, min(1.0, predicted))

# This is a configurable linear-regression implementation for our load-prediction module. We have not established that the paper specifies this exact regression equation. Before claiming an exact reproduction, we must verify the paper's load-prediction methodology.