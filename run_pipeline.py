import subprocess
import sys



# Pipeline Steps

STEPS = [
    [
        sys.executable,
        "src/make_data.py",
    ],
    [
        sys.executable,
        "src/load_db.py",
    ],
    [
        sys.executable,
        "src/etl.py",
    ],
]



# Run Pipeline

def main():

    print("=" * 60)
    print("E-COMMERCE ANALYTICS PIPELINE")
    print("=" * 60)

    for step_number, step in enumerate(STEPS, start=1):

        print("\n" + "-" * 60)
        print(
            f"STEP {step_number}/{len(STEPS)}"
        )
        print("-" * 60)

        print("Running:")
        print(" ".join(step))

        result = subprocess.run(
            step,
            check=False,
        )

        if result.returncode != 0:

            print("\n" + "=" * 60)
            print("PIPELINE FAILED")
            print("=" * 60)

            print(
                f"\nFailed step: "
                f"{step_number}/{len(STEPS)}"
            )

            print(
                f"Command: {' '.join(step)}"
            )

            print(
                f"Exit code: "
                f"{result.returncode}"
            )

            sys.exit(
                result.returncode
            )

        print(
            f"\nStep {step_number} completed successfully."
        )

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nGenerated outputs:")

    print(
        "  - Raw datasets: "
        "data/raw/"
    )

    print(
        "  - Processed datasets: "
        "data/processed/"
    )

    print("\n")



# Entry Point


if __name__ == "__main__":
    main()
