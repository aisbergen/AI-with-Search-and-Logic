#Meeting Scheduling Problem from csp.lib
model = """
language ESSENCE' 1.0

given m: int $meetings
given a: int $num of agents
given l: int $num of locations
given i: int $duration
given max_time_slot: int $Maximum possible time slot for a meeting to end.

given T: matrix indexed by [int(1..m)] of int(1..i) $Each meeting mi is associated with a set si of agents in S,that attend it
given S : matrix indexed by [int(1..m)] of set of int(1..a) $each agent has a set of meetings that it must attend
given location : matrix indexed by [int(1..m)] of int(1..l) $Each meeting is associated with a location
given travel : matrix indexed by [int(1..l), int(1..l)] of int(0..10) $travel time

find start_time: matrix indexed by [int(1..m)] of int(0..max_time_slot) $1..m indices, each index shows single set of value range 0 to max_time_slot

such that
   forAll i, j : int(1..m) where i < j . (
    if (S[i] \/ S[j] != {}) then
      (start_time[i] + T[i] + travel[location[i], location[j]] <= start_time[j])
            \/
            (start_time[j] + T[j] + travel[location[j], location[i]] <= start_time[i])
        )
   ) -- If meeting i ends, and an agent has to travel to meeting j, then meeting j
            -- can only start after meeting i finishes PLUS travel time.
            -- This applies bidirectionally if agents can go from i to j or j to i.
"""

param = """
language ESSENCE' 1.0
"""


solve(model, param)
