# Attack Graph Design

The directed graph uses observable entities as nodes: threat indicator/IP, user account, source asset, vulnerability, and target asset. Edges encode defensive relationships such as `observes user account`, `accesses asset`, `exposes vulnerability`, and `connects to`. Graph edges are stored with node type/value and target for dashboard rendering. Path enumeration is bounded to six hops and uses simple paths, avoiding cycles and unbounded traversal.
