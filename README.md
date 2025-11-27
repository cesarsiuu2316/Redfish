# Redfish

EthGlobal Hackathon 2025, Buenos Aires.

## Introduction
DeFi protocols are constantly under siege. From liquidity vampires (LVR) to flashloan exploiters, malicious actors drain value from Liquidity Providers (LPs). Traditional defenses are rigid: static allowlists or centralized monitoring. Redfish changes the game. It is a trustless anomaly detection system that brings the power of machine learning onchain, atomically verified via Zero Knowledge Proofs.

## What It Does
Redfish acts as an intelligent filter for transaction flow.

*   Real-time Sanitization: A Uniswap v4 Hook that checks every swap against an ML model. If the transaction's "anomaly score" (reconstruction error) is too high—indicating flash-loan manipulation or toxic flow—it is rejected *before* it touches the pool.
*   Historical Reputation: Uses vlayer Time Travel to verify a wallet's behavior over time (e.g., frequency of interaction, past deployments), feeding this "reputation score" into the ZKML model as a feature.

## Stack

*   EZKL Runs a lightweight Autoencoder circuit. We train the model on "normal" market behavior. When a transaction occurs, EZKL generates a proof that the transaction fits (or breaks) this normal pattern. The model logic is hidden (privacy-preserving), but its execution is verifiable.
*   vlayer: Smart contracts have amnesia; they only see the current block. Redfish uses vlayer's Time Travel to trustlessly prove historical states (e.g., "Average balance over the last 1000 blocks"), enriching the ML model's input vectors without trusted off-chain indexers.
*   Uniswap v4 Hook: The integration point. It verifies the ZK proof from EZKL/vlayer. If the proof is valid and the score is safe, the swap proceeds. If not, Redfish reels it in.

## Why ZKML?

*   Computational Expressivity: We can run complex outlier detection algorithms (Isolation Forests, Autoencoders) that are too expensive for raw Solidity.
*   Privacy & Security: The model's weights and sensitivity thresholds can remain private. Attackers cannot "game" the parameters because they don't know the exact boundaries of the detection logic, only that a proof of safety is required.
*   Trustlessness: No centralized API decides what is a "hack." The decision is mathematical, verifiable, and executed atomically onchain.

## 📊 Circuit Metadata (Latest Run: 2025-11-23 02:11:29)

| Artifact | Size | Description |
|----------|------|-------------|
|  | 608K | Compiled Circuit |
|  | 749M | Proving Key (Not in Repo) |
|  | 212K | Verification Key |
|  | 8.1M | Structured Reference String |
|  | 36K | Sample Proof |
