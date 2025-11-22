import ezkl
import asyncio
from ezkl_config import *

async def main():
    logger.info("--- Step 4: SRS & Keys ---")
    
    # Get SRS
    res = await ezkl.get_srs(settings_path=str(SETTINGS_PATH), logrows=None, srs_path=str(SRS_PATH))
    if res:
        logger.info("SRS ready")
    else:
        logger.error("Failed to get SRS")
        return

    # Setup
    # Trying 'model' argument instead of 'compiled_circuit' based on error
    # Assuming signature: setup(model, vk_path, pk_path, srs_path)
    
    try:
        res = ezkl.setup(
            model=str(COMPILED_PATH), # Pass compiled circuit path as 'model'
            vk_path=str(VK_PATH),
            pk_path=str(PK_PATH),
            srs_path=str(SRS_PATH)
        )
    except TypeError:
        # Fallback: positional arguments if named args fail
        res = ezkl.setup(
            str(COMPILED_PATH),
            str(VK_PATH),
            str(PK_PATH),
            str(SRS_PATH)
        )

    if res:
        logger.info("Keys generated")
        log_resource_usage("Setup")
    else:
        logger.error("Setup failed")

if __name__ == "__main__":
    asyncio.run(main())
