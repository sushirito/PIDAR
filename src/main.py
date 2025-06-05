import sys
from src.data_prep import verify_inputs
from src.train import train_all_lrs
from src.predict import predict_with_best
from src.archive import archive_predictions

def main():
    # Step 1: Make sure all input paths are good to go
    try:
        verify_inputs()
    except Exception as e:
        print("Hmm, input verification failed:", e)
        sys.exit(1)  # Bail out if inputs are messed up

    # Step 2: Start training with different learning rates
    print(">>> Kicking off training... could take a while.")
    train_all_lrs()

    # Step 3: Inference time! Using the best trained model.
    print("\n>>> Running inference on test set.")
    predict_with_best()

    # Step 4: Tidy up by archiving the results
    print("\n>>> Archiving predictions for later.")
    archive_predictions()

    print("\nAll done!")

# Note: Leaving this here in case we want to run this as a script
if __name__ == "__main__":
    main()