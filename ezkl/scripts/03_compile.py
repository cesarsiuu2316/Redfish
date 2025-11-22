import ezkl
from ezkl_config import *

def main():
    logger.info("--- Step 3: Compilation ---")
    ezkl.compile_circuit(
        model=str(MODEL_PATH),
        compiled_circuit=str(COMPILED_PATH),
        settings_path=str(SETTINGS_PATH)
    )
    logger.info(f"Compiled to {COMPILED_PATH}")
    log_resource_usage("Compile")

if __name__ == "__main__":
    main()
