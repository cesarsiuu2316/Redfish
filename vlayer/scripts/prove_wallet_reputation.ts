import 'dotenv/config';
import * as fs from 'fs';
import { decodeAbiParameters } from 'viem';

interface Presentation {
  success: boolean;
  data: string;
  version?: string;
  meta?: {
    notaryUrl?: string;
  };
}

interface CompressedData {
  success: boolean;
  data: {
    zkProof: string;
    journalDataAbi: string;
  };
}

interface ProofData {
  success: boolean;
  data: {
    zkProof: string;
    journalDataAbi: string;
  };
}

const walletAddress = process.argv[2] || process.env.TARGET_WALLET_ADDRESS;

if (!walletAddress) {
  console.error('Error: No wallet address provided');
  console.log('Usage: npm run prove <wallet_address>');
  process.exit(1);
}

console.log('\n=== Generating Wallet Reputation Proof ===');
console.log('Target Wallet: ' + walletAddress);

const baseUrl = 'https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=' + walletAddress + '&tag=latest';
const apiKey = process.env.ETHERSCAN_API_KEY;
const etherscanApiUrl = apiKey ? baseUrl + '&apikey=' + apiKey : baseUrl;

console.log('[1/4] Calling vlayer web-prover API...');

const response = await fetch('https://web-prover.vlayer.xyz/api/v1/prove', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-client-id': process.env.WEB_PROVER_API_CLIENT_ID || '',
    'Authorization': 'Bearer ' + process.env.WEB_PROVER_API_SECRET,
  },
  body: JSON.stringify({
    url: etherscanApiUrl,
    headers: []
  })
});

if (!response.ok) {
  const errorText = await response.text();
  console.error('Web Prover API error:', errorText);
  throw new Error('HTTP error! status: ' + response.status);
}

const data = await response.json() as Presentation;
console.log('✓ TLS-notarized proof received');

const presentation = data;

if (!presentation || !presentation.data) {
  throw new Error('No presentation data found in response');
}

console.log('[2/4] Extracting balance data via JMESPath...');

const extractConfig = {
  "response.body": {
    "jmespath": ["result"]
  }
};

console.log('✓ Extract config ready');

console.log('[3/4] Compressing web proof via zk-prover API...');
console.log('   (This may take 60-120 seconds)');

const requestBody = {
  presentation,
  extraction: extractConfig
};

const zkProverUrl = process.env.ZK_PROVER_API_URL || 'https://zk-prover.vlayer.xyz/api/v0';
const compressResponse = await fetch(zkProverUrl + '/compress-web-proof', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-client-id': process.env.WEB_PROVER_API_CLIENT_ID || '',
    'Authorization': 'Bearer ' + process.env.WEB_PROVER_API_SECRET,
  },
  body: JSON.stringify(requestBody),
  signal: AbortSignal.timeout(120000)
});

if (!compressResponse.ok) {
  const errorText = await compressResponse.text();
  console.error('ZK Prover API error:', errorText);
  throw new Error('HTTP error! status: ' + compressResponse.status);
}

const compressedData = await compressResponse.json() as CompressedData;
console.log('✓ ZK proof generated successfully');

console.log('[4/4] Decoding and saving proof...');

try {
  const journalDataAbi = compressedData.data.journalDataAbi as `0x${string}`;
  
  const decoded = decodeAbiParameters(
    [
      { type: 'bytes32', name: 'notaryKeyFingerprint' },
      { type: 'string', name: 'method' },
      { type: 'string', name: 'url' },
      { type: 'uint256', name: 'timestamp' },
      { type: 'bytes32', name: 'queriesHash' },
      { type: 'string', name: 'balance' }
    ],
    journalDataAbi
  );
  
  const [notaryKeyFingerprint, method, url, timestamp, queriesHash, balance] = decoded;
  
  console.log('\n--- Decoded Wallet Reputation Data ---');
  console.log('Wallet Address: ' + walletAddress);
  console.log('Balance (wei): ' + balance);
  
  const balanceBigInt = BigInt(balance as string);
  const ethAmount = balanceBigInt / BigInt(10 ** 18);
  const remainder = balanceBigInt % BigInt(10 ** 18);
  console.log('Balance (ETH): ' + ethAmount.toString() + '.' + remainder.toString().padStart(18, '0').slice(0, 4) + ' ETH');
  
  console.log('Timestamp: ' + new Date(Number(timestamp) * 1000).toISOString());
  console.log('Notary Fingerprint: ' + notaryKeyFingerprint);
  console.log('Queries Hash: ' + queriesHash);
  console.log('--------------------------------------\n');
} catch (error) {
  console.error('Error decoding journalDataAbi:', (error as Error).message);
  console.log('Proof was generated successfully but could not decode data.');
}

const proofData: ProofData = {
  success: compressedData.success,
  data: {
    zkProof: compressedData.data.zkProof,
    journalDataAbi: compressedData.data.journalDataAbi
  }
};

const proofsDir = './proofs';
if (!fs.existsSync(proofsDir)) {
  fs.mkdirSync(proofsDir, { recursive: true });
}

const proofFilePath = proofsDir + '/wallet_reputation_proof.json';
fs.writeFileSync(proofFilePath, JSON.stringify(proofData, null, 2));

console.log('✓ Proof saved to: ' + proofFilePath);
console.log('\n=== Proof Generation Complete ===\n');
