""" This module provides a class to generate
    parametrised distributions for simulation purposes
    
    It is still in experimental stage and may not be fully functional
    or tested. Use at your own risk.
    
    
    """

import math
import numpy as np

import matplotlib.pyplot as plt
from scipy.stats import lognorm, norm, uniform, triang


class simulation:
    """convenience class to generate parametrised distributions"""

    def __init__(
        self,
        mean=None,
        std_dev=None,
        lower_bound=None,
        upper_bound=None,
        probability=None,
        seed=None,
    ):
        try:
            assert (
                lower_bound is None and upper_bound is None and probability is None
            ) or (lower_bound < upper_bound and probability > 0 and probability < 1.0)
        except AssertionError:
            print("Ensure you provide either all LB+UB+Prob or provide Mean+Std_dev")
        try:
            assert (mean is None and std_dev is None) or (mean != 0 and std_dev > 0)
        except AssertionError:
            print("Error in the parameters mean and std_dev:", mean, std_dev)
        self.mean = mean  # mean
        self.std_dev = std_dev  # standard deviation
        self.seed = seed
        self.samples = None
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.probability = probability  # probability of the confidence interval
        np.random.seed(self.seed)
        self.random_series = None

    def generate(self, size=1, random_series=None):
        """generate by default for normal distribution"""
        alpha = 1 - self.probability
        z = norm.ppf(1 - alpha / 2)
        if self.mean is None:
            self.mean = (self.upper_bound + self.lower_bound) / 2
        if self.std_dev is None:
            self.std_dev = (self.upper_bound - self.lower_bound) / (2 * z)
        if (random_series is not None) and (len(random_series) >= size):
            print("Random series provided")
            self.random_series = random_series[:size]
        else:
            # uniform distribution 0,1
            self.random_series = np.random.uniform(0, 1, size)

        self.samples = norm.ppf(q=self.random_series, loc=self.mean, scale=self.std_dev)
        self.simulated_mean = np.mean(self.samples)
        self.simulated_median = np.median(self.samples)
        self.simulated_std_dev = np.std(self.samples)
        self.size = size

    def plot_log_scale(self):
        """plot the histogram of the samples in log scale"""
        plt.hist(self.samples, bins=100, edgecolor="k", alpha=0.7)
        plt.title("Monte Carlo Simulation")
        plt.xlabel("Values")
        plt.ylabel("Frequency")
        plt.xscale("log")
        plt.yscale("log")
        plt.show()

    def plot(self, bins=100):
        """plot the histogram of the samples"""
        hist, bins, _ = plt.hist(self.samples, bins=bins, edgecolor="k", alpha=0.7)
        plt.title("Monte Carlo Simulation")
        plt.xlabel("Values")
        plt.ylabel("Frequency")
        # Calculate the scaling factor
        bin_width = bins[1] - bins[0]
        scaling_factor = self.size * bin_width
        # count of observations within confidence interval
        num_within_interval = np.sum(
            (self.samples >= self.lower_bound) & (self.samples <= self.upper_bound)
        )
        # Calculate the proportion of observations within the confidence interval
        proportion_within_interval = num_within_interval / self.size

        plt.axvline(
            x=self.lower_bound,
            color="r",
            linestyle="dashed",
            linewidth=2,
            label=f"Lower bound ({self.lower_bound})",
        )
        plt.axvline(
            x=self.upper_bound,
            color="g",
            linestyle="dashed",
            linewidth=2,
            label=f"Upper bound ({self.upper_bound})",
        )
        plt.axvline(
            x=self.mean,
            color="b",
            linestyle="dashed",
            linewidth=2,
            label=f"Mean ({int(self.mean)})",
        )

        # add mean, median and std deviation to the plot as floating box
        plt.text(
            0.8,
            0.9,
            f"Mean: {self.simulated_mean:,.2f}\nMedian: {self.simulated_median:,.2f}\nStd Dev: {self.simulated_std_dev:,.2f}\nProportion within interval:{proportion_within_interval:.2}",
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
        )
        plt.show()

    def statistics(self):
        """returns a dictionary with all the statistics"""
        return {
            "mean": self.simulated_mean,
            "median": self.simulated_median,
            "std_dev": self.simulated_std_dev,
        }


class simulation_lognormal(simulation):
    """Generates lognormal distribution with the lower and upper bound provided"""

    def __init__(
        self,
        mean=None,
        std_dev=None,
        lower_bound=None,
        upper_bound=None,
        probability=None,
        seed=None,
    ):
        super().__init__(
            mean=mean,
            std_dev=std_dev,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            probability=probability,
            seed=seed,
        )

    def generate(
        self, size=1, random_series=None
    ):  # generate the lognormal distribution
        assert size > 0, "size must be greater than 0"
        if (random_series is not None) and (len(random_series) >= size):
            self.random_series = random_series[:size]
        else:
            # uniform distribution 0,1
            self.random_series = np.random.uniform(0, 1, size)

        if self.mean is not None and self.std_dev is not None:
            # self.samples = np.random.lognormal(self.mean, self.std_dev, size)
            self.samples = lognorm(self.mean, scale=self.std_dev).ppf(
                self.random_series
            )
        elif self.lower_bound is not None and self.upper_bound is not None:
            # Convert the confidence level to a z-score
            z_score = norm.ppf((1 + self.probability) / 2)
            # Calculate the log-transformed mean and confidence interval
            log_lower_bound = np.log(self.lower_bound)
            log_upper_bound = np.log(self.upper_bound)
            # Calculate the mean and standard deviation of the underlying normal distribution
            mu_Y = (log_lower_bound + log_upper_bound) / 2
            sigma_Y = (log_upper_bound - log_lower_bound) / (2 * z_score)
            # samples_normal = np.random.normal(mu_Y, sigma_Y, size)
            # Theoretical mean from a lognormal based on the upper and lower band

            lognormal_mean = np.exp(mu_Y + (sigma_Y**2) / 2)
            self.mean = lognormal_mean
            # We now transform that normal into exp to generate the lognormal distribution
            samples_normal = norm.ppf(q=self.random_series, loc=mu_Y, scale=sigma_Y)
            self.samples = np.exp(samples_normal)
        else:
            raise ValueError(
                "Either mean and sigma or lower and upper bounds must be provided"
            )

        self.simulated_mean = np.mean(self.samples)
        self.simulated_median = np.median(self.samples)
        self.simulated_std_dev = np.std(self.samples)
        self.size = size


class simulation_uniform(simulation):
    """Generates uniform distribution with the lower and upper bound provided"""

    def __init__(self, lower_bound=None, upper_bound=None, probability=None, seed=None):
        mean = (lower_bound + upper_bound) / 2
        std_dev = (upper_bound - lower_bound) / math.sqrt(12)
        super().__init__(
            mean=mean,
            std_dev=std_dev,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            probability=probability,
            seed=seed,
        )

    def generate(self, size=1, random_series=None):  # generate the uniform distribution
        assert size > 0, "size must be greater than 0"
        if (random_series is not None) and (len(random_series) >= size):
            self.random_series = random_series[:size]
        else:
            # uniform distribution 0,1
            self.random_series = np.random.uniform(0, 1, size)

        if self.lower_bound is not None and self.upper_bound is not None:
            # self.samples = np.random.uniform(self.lower_bound, self.upper_bound, size)
            self.samples = uniform.ppf(
                q=self.random_series, loc=self.mean, scale=self.std_dev
            )
        else:
            raise ValueError("Both lower and upper bounds must be provided")

        self.simulated_mean = np.mean(self.samples)
        self.simulated_median = np.median(self.samples)
        self.simulated_std_dev = np.std(self.samples)
        self.size = size


class simulation_triangular(simulation):
    """Generates triangular distribution with the lower and upper bound provided"""

    def __init__(
        self, mode=None, lower_bound=None, upper_bound=None, probability=None, seed=None
    ):
        if lower_bound is None or upper_bound is None or mode is None:
            raise ValueError(
                "All mode, lower and upper bounds must be provided for the triangular distribution"
            )
        std_dev = math.sqrt(
            (
                lower_bound**2
                + upper_bound**2
                + mode**2
                - lower_bound * upper_bound
                - lower_bound * mode
                - upper_bound * mode
            )
            / 18
        )
        mean = (lower_bound + upper_bound + mode) / 3
        super().__init__(
            mean=mean,
            std_dev=std_dev,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            probability=probability,
            seed=seed,
        )
        self.mode = mode
        self.mode_scaled = (mode - lower_bound) / (
            upper_bound - lower_bound
        )  # c parameter for the triangular distribution

    def generate(
        self, size=1, random_series=None
    ):  # generate the triangular distribution
        assert size > 0, "size must be greater than 0"
        if (random_series is not None) and (len(random_series) >= size):
            self.random_series = random_series[:size]
        else:
            # uniform distribution 0,1
            self.random_series = np.random.uniform(0, 1, size)

        if (
            self.mode is not None
            and self.lower_bound is not None
            and self.upper_bound is not None
        ):
            # self.samples = np.random.triangular(left=self.lower_bound, mode=self.mode, right=self.upper_bound, size=size)
            self.samples = triang.ppf(
                q=self.random_series,
                c=self.mode_scaled,
                loc=self.lower_bound,
                scale=self.upper_bound - self.lower_bound,
            )

        else:
            raise ValueError(
                "All mode, lower and upper bounds must be provided for the triangular distribution"
            )

        self.simulated_mean = np.mean(self.samples)
        self.simulated_median = np.median(self.samples)
        self.simulated_std_dev = np.std(self.samples)
        self.size = size
