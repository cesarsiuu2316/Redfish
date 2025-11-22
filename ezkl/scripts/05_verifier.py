import ezkl
import shutil
import asyncio
from ezkl_config import *

async def main():
    logger.info("--- Step 5: Verifier Contract ---")
    
    # Create EVM Verifier (Async in some versions)
    # If this fails, we try sync. But error log showed it needed loop previously?
    # Actually, error was in 04_setup.py at get_srs. 05 might not need async if create_evm_verifier is sync.
    # But let's wrap in async just in case it changed.
    
    res = await ezkl.create_evm_verifier(
        vk_path=str(VK_PATH),
        settings_path=str(SETTINGS_PATH),
        sol_code_path=str(VERIFIER_PATH),
        srs_path=str(SRS_PATH)
    )
    
    if res:
        logger.info(f"Verifier saved to {VERIFIER_PATH}")
        # Copy to src
        shutil.copy(VERIFIER_PATH, CONTRACTS_SRC / "Verifier.sol")
        logger.info(f"Copied to {CONTRACTS_SRC}")
    else:
        logger.error("Verifier creation failed")

if __name__ == "__main__":
    asyncio.run(main())
