import ezkl
from ezkl_config import *

def main():
    logger.info("--- Step 2: Settings & Calibration ---")
    
    py_run_args = ezkl.PyRunArgs()
    py_run_args.input_visibility = "public"
    py_run_args.output_visibility = "public"
    py_run_args.param_visibility = "fixed"

    ezkl.gen_settings(
        model=str(MODEL_PATH),
        output=str(SETTINGS_PATH),
        py_run_args=py_run_args
    )
    
    ezkl.calibrate_settings(
        data=str(INPUT_PATH),
        model=str(MODEL_PATH),
        settings=str(SETTINGS_PATH),
        target="resources",
    )
    logger.info("Settings generated and calibrated")
    log_resource_usage("Settings")

if __name__ == "__main__":
    main()
