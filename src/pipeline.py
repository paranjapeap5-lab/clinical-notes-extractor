import pandas as pd

from src import config
from src.claude_client import ClaudeClient
from src.extractor import extract_demographics


def load_notes(n: int) -> pd.DataFrame:
    print(f"Loading {n} notes from Hugging Face...")
    df = pd.read_json(config.DATASET, lines=True)  # config.DATASET
    return df.sample(n=n, random_state=config.RANDOM_STATE).reset_index(drop=True)


def extract_all(notes: pd.DataFrame, client: ClaudeClient) -> pd.DataFrame:
    results = []
    for i, row in notes.iterrows():
        result = extract_demographics(row[config.NOTE_COLUMN], client)
        if result["status"] == "ok":
            results.append(result["data"])
            print(f"  extracted {i + 1}/{len(notes)}")
        else:
            results.append({"error_stage": result["stage"]})
            print(
                f"  extracted {i + 1}/{len(notes)}  ⚠️  ERROR "
                f"({result['stage']}): {result['error']}"
            )
            print(f"     raw response: {result['raw'][:200]}")
    return pd.DataFrame(results)


def main():
    notes = load_notes(config.N_NOTES)  # config.N_NOTES
    client = ClaudeClient()
    extracted = extract_all(notes, client)

    notes.to_csv(f"{config.OUTPUT_DIR}/original.csv", index=False)  # config.OUTPUT_DIR
    extracted.to_csv(f"{config.OUTPUT_DIR}/demographics.csv", index=False)

    combined = pd.concat([notes.reset_index(drop=True), extracted], axis=1)
    combined.to_csv(f"{config.OUTPUT_DIR}/combined.csv", index=False)

    print(f"\nDone. Wrote 3 files to {config.OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
