
import random

from .models.entities import Task, Resource
from .models.priority_model import DynamicPriorityModel
from .models.load_predictor import LoadPredictor

from .task_generator import TaskGenerator
from .resource_manager import ResourceManager
from .resource_allocator import ResourceAllocator
from .energy_manager import EnergyManager
from .load_balancer import LoadBalancer
from .metrics import Metrics


class DPTARASimulator:
    """
    Central simulation controller for the DPTARA framework.

    Coordinates task generation, resource management,
    priority calculation, allocation, energy management,
    load balancing, and performance evaluation.
    """

    def __init__(
        self,
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42
    ):

        if simulation_duration <= 0:
            raise ValueError(
                "Simulation duration must be positive."
            )

        # Simulation configuration
        self.simulation_duration = simulation_duration
        self.arrival_rate = arrival_rate
        self.seed = seed

        # Reproducible random number generator
        self.rng = random.Random(seed)

        # Initialize task generator
        self.task_generator = TaskGenerator(
            arrival_rate=arrival_rate,
            seed=seed
        )

        # Initialize resource manager
        self.resource_manager = ResourceManager()

        # Initialize resource allocator
        self.resource_allocator = ResourceAllocator(
            self.resource_manager
        )

        # Initialize priority model
        self.priority_model = DynamicPriorityModel(
            alpha=1.0,
            beta=1.0,
            gamma=1.0
        )

        # Initialize load predictor
        self.load_predictor = LoadPredictor()

        # Initialize energy manager
        self.energy_manager = EnergyManager()

        # Initialize load balancer
        self.load_balancer = LoadBalancer()

        # Initialize metrics
        self.metrics = Metrics()

        # Store simulation tasks
        self.tasks = []

        print("DPTARA Simulator initialized successfully.")

    def initialize_resources(self):
        """
        Initialize 10 edge servers and 1 cloud server
        using the hardware configuration documented
        in the DPTARA simulation parameters.
        """

        # Initialize 10 edge servers
        for i in range(1, 11):

            cpu_capacity = self.rng.randint(500, 3000)

            resource = Resource(
                resource_id=f"E{i}",
                resource_type="edge",
                capacity=cpu_capacity,
                current_load=0.0,
                processing_speed_mips=cpu_capacity,
                power_consumption_w=50.0,
                network_latency_ms=round(
                    self.rng.uniform(5, 10), 2
                )
            )

            self.resource_manager.register_resource(resource)

        # Initialize 1 cloud server
        cloud_capacity = self.rng.randint(2000, 10000)

        cloud = Resource(
            resource_id="C1",
            resource_type="cloud",
            capacity=cloud_capacity,
            current_load=0.0,
            processing_speed_mips=cloud_capacity,
            power_consumption_w=200.0,
            network_latency_ms=round(
                self.rng.uniform(50, 100), 2
            )
        )

        self.resource_manager.register_resource(cloud)

        return self.resource_manager.get_all_resources()
