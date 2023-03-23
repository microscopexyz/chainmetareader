# Schema of GoPlus's Metadata
| **Field Name** | **Data Type** |                     **Description**                     |                **Example**                 |
|----------------|---------------|:-------------------------------------------------------:|:------------------------------------------:|
| submitted_by   | String        |                     Provider's name                     |                   GoPlus                   |
| address        | String        |                         Address                         | 0x333f2e9f074de56d3ed6a0518c3d0df418692b63 |
| entity         | String        |              Whether the address is risky               |             High Risk Address              |
| categories     | Array         | The risk type of the address，maybe have multiple values |      ["Address Related to Honeypot"]       |
| updated_at     | Datetime      |              The last update time of data               |                 2023-03-01                 |


## Schema of Categories
| Categories Items            | Description                                                                                 |
|-----------------------------|---------------------------------------------------------------------------------------------|
| Address Related to Honeypot | It describes whether this address is related to honeypot tokens or has created scam tokens. |
| Phishing Activities         | It describes whether this address has implemented phishing activities.                      |
| Black Mail Activities       | It describes whether this address has implemented blackmail activities.                     |
| Stealing Attack             | It describes whether this address has implemented stealing attacks.                         |
| Fake KYC                    | It describes whether this address is involved in fake KYC.                                  |
| Malicious Mining Activities | It describes whether this address is involved in malicious mining activities.               |
| Darkweb Transactions        | It describes whether this address is involved in darkweb transactions.                      |
| Cybercrime                  | It describes whether this address is involved in cybercrime.                                |
| Money Laundering            | It describes whether this address is involved in money laundering.                          |
| Financial Crime             | It describes whether this address is involved in financial crime.                           |
| Mixer                       | It describes whether this address is coin mixer address.                                    |
| Sanctioned                  | It describes whether this address is coin sanctioned address.                               |
| Other                       | It describes whether this address is suspected of malicious behavior.                       |
