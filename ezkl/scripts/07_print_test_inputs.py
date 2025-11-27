import json
import os

def main():
    proof_path = '../build/proof.json'
    with open(proof_path, 'r') as f:
        proof_data = json.load(f)
    
    hex_proof = proof_data['hex_proof']
    instances = proof_data['instances'][0]
    
    # Generate Solidity file content directly
    sol_content = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import \"forge-std/Test.sol\";
import \"../src/Verifier.sol\";

contract VerifierTest is Test {{
    Halo2Verifier public verifier;

    function setUp() public {{
        verifier = new Halo2Verifier();
    }}

    function test_VerifyProof() public {{
        bytes memory proof = hex\"{hex_proof[2:]}\";
        
        uint256[] memory instances = new uint256[]({len(instances)});
"""
    
    for i, val in enumerate(instances):
        # Handle hex string from JSON (e.g. '661a...')
        if val.startswith('0x'):
            clean_val = val[2:]
        else:
            clean_val = val
        
        # Convert to 0x... format for Solidity
        sol_content += f'        instances[{i}] = 0x{clean_val};\n'

    sol_content += """
        try verifier.verifyProof(proof, instances) returns (bool success) {{
            assertTrue(success, \"Proof verification returned false\");
        }} catch Error(string memory reason) {{
            console.log(\"Revert Reason:\", reason);
            assertTrue(false, \"Verification reverted\");
        }} catch (bytes memory) {{
            console.log(\"Unknown Revert\");
            assertTrue(false, \"Verification reverted with unknown error\");
        }}
    }}
}}
"""
    
    # Write directly to the test file
    with open('../../test/Verifier.t.sol', 'w') as f:
        f.write(sol_content)
    print("Updated test/Verifier.t.sol with hardcoded inputs.")

if __name__ == "__main__":
    main()
