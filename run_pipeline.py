
from generator.simulator import generate_dataset
from validator.validator import validate_dataset
from analysis.distribution import analyze_distribution
from analysis.timeseries import analyze_timeseries
from analysis.volatility import analyze_volatility
from report.generate_report import generate_report


def main():
    print("Research Pipeline v2.0")

    dataset = generate_dataset(rows=1000000)

    validation = validate_dataset(dataset)

    distribution = analyze_distribution(dataset)

    timeseries = analyze_timeseries(dataset)

    volatility = analyze_volatility(dataset)

    generate_report(
        validation=validation,
        distribution=distribution,
        timeseries=timeseries,
        volatility=volatility
    )

    print("Pipeline Finished")


if __name__ == "__main__":
    main()
