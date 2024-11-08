# Bitcoin custom address generator
The Bitcoin Custom Address Generator is a Python-based tool designed to create personalized Bitcoin addresses that match user-defined criteria, such as specific prefixes or patterns. By leveraging cryptographic libraries and custom algorithms, this tool allows users to generate vanity Bitcoin addresses that meet their desired format, while adhering to Bitcoin's security standards and cryptographic requirements.

# Key Features:
### Pattern Matching for Custom Addresses:
Users can specify custom patterns (like starting with "1Love" or containing specific characters) for the Bitcoin address. The generator will continuously create and verify addresses until it finds one that matches the user's criteria.

### Efficiency and Speed Optimization:
Generating custom Bitcoin addresses can be computationally intensive. The program employs optimized algorithms and libraries (e.g., ECDSA, secp256k1) to ensure faster address generation, even for complex patterns.

### User-Friendly Interface:
An intuitive command-line interface allows users to specify pattern requirements and receive feedback on progress. The interface can also include options for setting difficulty levels based on pattern complexity.

### Multi-Threading and Parallel Processing:
For high-performance, the program can utilize multi-threading, distributing workload across multiple processor cores. This significantly reduces the time required to find a matching address, especially with complex patterns.

### Address Validity Checks:
Ensures that generated addresses are valid under the Bitcoin protocol and follow the correct checksum standards, guaranteeing that each address could securely receive Bitcoin transactions.

### Secure Key Pair Generation:
Each generated address comes with a corresponding private key. The tool uses secure cryptographic methods to generate and protect these keys, allowing safe storage and usage.

## Usage
- `pip install -r requirements.txt`
- `python main.py`
- input your target ex. `1Love` or `1Love,1Git,bc1Love`
- Choose if you want to check for case sensitive (non-case-sensitive are found faster)
- Choose threads (10 - Good PC, <5 - Low PC)

## Info
- After an address is found it will save it in address.json with address, private key, wif, pubkey, pattern, timestamp
- If you have low performance PC or do not have time for searching you message me and I will search it for you.

## Pictures

![{C4BE66F1-2E45-4084-AC8C-83FDBFCCEDCF}](https://github.com/user-attachments/assets/888d7e96-c128-4499-9c29-34ae9c63e9ab)

