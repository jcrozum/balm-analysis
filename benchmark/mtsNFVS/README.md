# mtsNFVS

Boolean Networks (BNs) play a crucial role in modeling, analyzing, and controlling biological systems. 
One of the most important problems on BNs is to compute all the possible attractors of a BN. 
There are two popular types of BNs, Synchronous BNs (SBNs) and Asynchronous BNs (ABNs). 
Although ABNs are considered more suitable than SBNs in modeling real-world biological systems, their attractor computation is more challenging than that of SBNs. 
Several methods have been proposed for computing attractors of ABNs. 
However, none of them can robustly handle large and complex models. 
We here propose a novel method called mtsNFVS for exactly computing all the attractors of an ABN based on its minimal trap spaces, where a trap space is a subspace of state space that no path can leave. 
The main advantage of mtsNFVS lies in opening the chance to reach easier cases for the attractor computation. 

The Java version is for the conference paper (<https://doi.org/10.1145/3535508.3545520>).

For the journal version, please see the Python version.

