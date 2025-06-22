import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from model_maker import model_makings
from model_register import register_model
path=os.path.join("Data","Banking_Call_Data.xlsx")
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    try:
        logging.info("Starting ML pipeline for Bank Marketing Project...")
        
        model_makings(path)

        logging.info("Model training and MLflow logging completed successfully.")

        register_model()
        

        logging.info("Model registration completed.")

    except Exception as e:
        logging.error(f"Pipeline failed due to error: {e}")
