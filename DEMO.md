# Redfish Demo: Hybrid ZK Proof System

## Quick Start

### Run Full Demo
```bash
./demo_redfish.sh [WALLET_ADDRESS]
```

**Default wallet:** `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`

This demonstrates the complete hybrid proof flow:
1. **vlayer zkTLS**: Verify wallet balance from Etherscan (60-120s)
2. **Extract & normalize**: Convert balance to ML model input
3. **EZKL ZKML**: Generate ZK proof of ML inference (8s)
4. **On-chain verify**: Test with Foundry (optional)

---

## Architecture

```
┌─────────────────┐
│ Etherscan API   │
│ (Balance data)  │
└────────┬────────┘
         │ HTTPS + TLS notary
         v
┌─────────────────┐
│ vlayer zkTLS    │  ← 60-120s proof generation
│ Web Prover      │     (RISC Zero STARK)
└────────┬────────┘
         │ 1.3 KB proof
         v
┌─────────────────┐
│ Extract Balance │
│ Normalize value │
└────────┬────────┘
         │ feature[0]
         v
┌─────────────────┐
│ EZKL ML Model   │  ← 8s proof generation
│ (620K params)   │     (Halo2 PLONK)
└────────┬────────┘
         │ 34 KB proof
         v
┌─────────────────┐
│ Halo2Verifier   │  ← On-chain verification
│ (Solidity)      │     (~50K-100K gas on L2)
└─────────────────┘
```

---

## Manual Steps

### 1. Generate vlayer Proof

```bash
cd vlayer
npx tsx scripts/prove_wallet_reputation.ts <WALLET_ADDRESS>
```

**Output:** `proofs/wallet_reputation_proof.json` (1.3 KB)

---

### 2. Extract Balance & Create EZKL Input

```bash
python3 hybrid_proof_pipeline_fixed.py
```

This script:
- Reads `vlayer/proofs/wallet_reputation_proof.json`
- Extracts balance from journal data
- Normalizes: `(balance_eth - 50) / 250`
- Creates `ezkl/build/hybrid_input_fixed.json`

---

### 3. Generate EZKL Proof

```bash
cd ezkl
python3 generate_hybrid_proof.py
```

**Time:** ~8 seconds (0.6s witness + 7.4s proof)

**Output:** `build/hybrid_proof.json` (34 KB)

---

### 4. Test On-Chain Verification

```bash
forge test --match-test test_FullHybridProofFlow -vv
```

**Output shows:**
- Step-by-step proof flow
- vlayer zkTLS verification
- Balance extraction
- EZKL proof generation
- Halo2 on-chain verification
- Gas estimates

---

## Performance Metrics

| Component | Time | Size | Gas |
|-----------|------|------|-----|
| vlayer proof | 60-120s | 1.3 KB | - |
| Balance extraction | <1s | - | - |
| EZKL witness | 0.6s | 3.2 KB | - |
| EZKL proof | 7.6s | 34 KB | - |
| On-chain verify | <0.5s | - | 50K-100K (L2) |
| **Total** | **~80s** | **35 KB** | **50K-100K** |

---

## Project Structure

```
Redfish/
├── demo_redfish.sh                 # Main demo script
├── DEMO.md                         # This file
├── hybrid_proof_pipeline_fixed.py  # Extract balance, create input
├── vlayer/
│   ├── scripts/
│   │   └── prove_wallet_reputation.ts
│   └── proofs/
│       └── wallet_reputation_proof.json (1.3 KB)
├── ezkl/
│   ├── generate_hybrid_proof.py    # EZKL proof generation
│   ├── model/
│   │   └── fraud_model.onnx (620K params)
│   └── build/
│       ├── hybrid_input_fixed.json
│       ├── hybrid_witness_final.json (3.2 KB)
│       ├── hybrid_proof_final.json (34 KB)
│       ├── network.ezkl
│       ├── kzg.srs (8.4 MB)
│       ├── pk.key (749 MB)
│       └── vk.key (211 KB)
├── src/
│   └── Verifier.sol (Halo2Verifier, 105 KB)
└── test/
    ├── Verifier.t.sol
    └── HybridProofDemo.t.sol  # Demo test with console logs
```

---

## Test Scenarios

### Scenario 1: Full Hybrid Proof Flow

```bash
forge test --match-test test_FullHybridProofFlow -vv
```

Shows complete flow with console logging:
- [STEP 1] vlayer zkTLS proof details
- [STEP 2] Balance extraction process
- [STEP 3] EZKL proof generation metrics
- [STEP 4] Loading proof artifacts
- [STEP 5] On-chain verification result

---

## What We Prove

This system cryptographically proves:

1. **Data Authenticity (vlayer zkTLS)**
   - Wallet balance came from Etherscan API
   - TLS connection was authentic (notary verified)
   - Response was not tampered with

2. **Correct Computation (EZKL ZKML)**
   - ML model executed correctly on verified data
   - Balance was used as input feature[0]
   - Fraud score output is valid

3. **End-to-End Trustlessness**
   - No need to trust data provider
   - No need to trust ML inference
   - Everything verified cryptographically

---

## Requirements

- **Python 3.8+** with `ezkl` package
- **Node.js** for vlayer scripts
- **Foundry** (forge, anvil) for Solidity tests
- **~1GB disk space** for keys and proofs

---

## Troubleshooting

**"vlayer proof generation timeout"**
- Increase timeout in script
- Check Etherscan API access

**"EZKL proof generation failed"**
- Ensure `ezkl/build/` has all required files
- Check that keys match compiled circuit

**"Forge test failed"**
- Run `forge build` first
- Check `foundry.toml` fs_permissions includes `./ezkl/build/`

---

## Next Steps

1. **Deploy to testnet:**
   - Arbitrum Sepolia
   - Base Sepolia
   - Optimism Sepolia

2. **Integrate with DeFi:**
   - Uniswap V4 hooks for fraud detection
   - Dynamic fees based on fraud score
   - Transaction limits for risky wallets

3. **Scale with batching:**
   - Verify multiple proofs in one transaction
   - Amortize verification costs

---

For technical details, see:
- `README.md` - Project overview
- `AGENTS.md` - Technical deep dive
- `docs/` - Additional documentation
