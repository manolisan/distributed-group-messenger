# Distributed group messenger
Group messenger in large-scale distributed systems.

## Messages Ordering

### Fifo ordering
The message delivery order at each process should preserve the message sending order from every process. But each process can deliver in a different order.

For example: 

- P1: m0, m1, m2

- P2: m3, m4, m5

- P3: m6, m7, m8

One of the FIFO ordering would be: 

- P1: m0, m3, m6, m1, m2, m4, m7, m5, m8

- P2: m3, m0, m1, m4, m6, m7, m5, m2, m8

- P3: m6, m7, m8, m0, m1, m2, m3, m4, m5

### Total ordering 

Every process delivers all messages in the same order. Here we don't care about any causal relationship of messages and as long as every process follows a single order we are fine.

For example: 

- P1: m0, m1, m2

- P2: m3, m4, m5

- P3: m6, m7, m8

One of the TOTAL ordering would be: 

- P1: m8, m1, m2, m4, m3, m5, m6, m0, m7

- P2: m8, m1, m2, m4, m3, m5, m6, m0, m7

- P3: m8, m1, m2, m4, m3, m5, m6, m0, m7

#### Implmentation of total ordering
- Sequencer: depend on centralized node
- ISIS: distributed algorithm 

## Network protocol between nodes
- UDP or TCP
- Software multicast 
