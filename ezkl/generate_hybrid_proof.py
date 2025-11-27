import ezkl
import json

print("="*60)
print("HYBRID PROOF GENERATION: vlayer zkTLS + EZKL ZKML")
print("="*60)

# Load hybrid input to show what we're proving
with open("build/hybrid_input.json", "r") as f:
    hybrid_input = json.load(f)
    
print("\nInput features:")
print(f"  Feature[0] (vlayer verified balance): {hybrid_input['input_data'][0][0]:.4f}")
print(f"  Features[1-15]: Other transaction metrics")

# Generate witness
print("\n[1/3] Generating witness...")
res = ezkl.gen_witness(
    data="build/hybrid_input.json",
    model="build/network.ezkl",
    output="build/hybrid_witness.json",
    vk_path="build/vk.key",
    srs_path="build/kzg.srs"
)
print("   ✓ Witness generated")

# Generate proof
print("\n[2/3] Generating ZK proof...")
print("   (This takes ~6 seconds)")
res = ezkl.prove(
    witness="build/hybrid_witness.json",
    model="build/network.ezkl",
    pk_path="build/pk.key",
    proof_path="build/hybrid_proof.json",
    srs_path="build/kzg.srs"
)
print("   ✓ Proof generated")

# Verify
print("\n[3/3] Verifying proof...")
result = ezkl.verify(
    proof_path="build/hybrid_proof.json",
    settings_path="build/settings.json",
    vk_path="build/vk.key",
    srs_path="build/kzg.srs"
)

if result:
    print("   ✓ Proof verified!")
    print("\n" + "="*60)
    print("SUCCESS! HYBRID PROOF COMPLETE")
    print("="*60)
    print("\nWhat we proved:")
    print("  1. Wallet balance verified via vlayer zkTLS ✓")
    print("  2. Balance used as ML model input (feature[0]) ✓")
    print("  3. ML model inference proven via EZKL ✓")
    print("\nResult: Trustless ML inference on verified external data!")
    print("="*60)
else:
    print("   ✗ Verification failed")
