from benchmark_utils import ensure_workspace


def initialize():

    ensure_workspace()

    print(
        "✅ Benchmark workspace initialized."
    )


if __name__ == "__main__":
    initialize()